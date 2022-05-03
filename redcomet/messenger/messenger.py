from typing import Dict, List

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.messenger.address_cache import AddressCache
from redcomet.messenger.direct_message.manager import DirectMessageManager
from redcomet.messenger.inbox import InboxAbstract
from redcomet.messenger.outbox import Outbox
from redcomet.messenger.request import MessageForwardRequest


class Messenger(ActorAbstract, MessengerAbstract):
    def __init__(self, actor_id: str, inbox: InboxAbstract, outbox: Outbox, address_cache: AddressCache = None,
                 node_id: str = None, discovery: ActorDiscoveryRefAbstract = None):
        self._actor_id = actor_id
        self._inbox = inbox
        self._outbox = outbox
        self._node_id = node_id
        self._discovery = discovery

        self._address_cache = address_cache or AddressCache()
        self._pending_messages: Dict[str, List[MessageForwardRequest]] = {}
        self._direct_message_manager = DirectMessageManager()

    def assign_node_id(self, node_id: str):
        self._node_id = node_id
        self._outbox.assign_node_id(node_id)
        self._outbox.register_inbox(self._inbox, node_id)

    def bind_discovery(self, ref: ActorDiscoveryRefAbstract):
        self._discovery = ref

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if message.ref_id is not None:
            self._put_to_direct_message_box(message)
        elif isinstance(message, MessageForwardRequest):
            self._forward_or_query_address(message)
        elif self._discovery.call_on_query_address_response(message, self._query_address_response):
            pass
        else:
            raise NotImplementedError()

    def _forward_or_query_address(self, message: MessageForwardRequest):
        receiver = self._address_cache.get_address(message.receiver_id)
        if receiver is not None:
            self._forward(message, Address(self._node_id, message.sender_id), receiver)
        else:
            self._store_message(message, wait_for_address=message.receiver_id)
            self._query_address_request(message.receiver_id)

    def _forward(self, message: MessageForwardRequest, sender: Address, receiver: Address):
        self.send_packet(Packet(message.message, sender=sender, receiver=receiver))

    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        packet = Packet(MessageForwardRequest(message, sender_id, receiver_id),
                        sender=Address.on_local(sender_id),
                        receiver=Address.on_local(self._actor_id))

        self.send_packet(packet)

    def send_packet(self, packet: Packet):
        self._outbox.send(packet)

    def make_connection_to(self, other: MessengerAbstract):
        if other is self:
            raise NotImplementedError
        if not isinstance(other, Messenger):
            raise TypeError("Messenger can only connect with another messenger")
        self._outbox.register_inbox(other._inbox, other.node_id)

    def _store_message(self, message: MessageForwardRequest, wait_for_address: str):
        self._pending_messages[wait_for_address] = self._pending_messages.get(wait_for_address, []) + [message]

    def _query_address_request(self, target: str):
        self._discovery.query_address(target, self._node_id, self._actor_id)

    def _query_address_response(self, target: str, address: Address):
        if address is not None:
            self._address_cache.update_cache(address)
            for message in self._pending_messages.get(target, []):
                self._forward(message, Address(self._node_id, message.sender_id), address)
        self._pending_messages[target] = []

    @property
    def actor_id(self) -> str:
        return self._actor_id

    @property
    def node_id(self) -> str:
        return self._node_id

    def create_direct_message_box(self) -> DirectMessageBoxRefAbstract:
        return self._direct_message_manager.create_message_box()

    def _put_to_direct_message_box(self, message: MessageAbstract):
        box = self._direct_message_manager.get_message_box(message.ref_id)
        if box is None:
            return
        box.put(message)

    def start_receive_loop(self):
        self._inbox.receive_loop()

    def stop_receive_loop(self):
        self._inbox.stop_receive_loop()

    def close(self):
        self._inbox.close()
