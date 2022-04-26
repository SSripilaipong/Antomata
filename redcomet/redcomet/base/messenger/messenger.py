from typing import Dict, List

from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.query import QueryAddressRequest, QueryAddressResponse
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.address_cache import AddressCache
from redcomet.base.messenger.request import MessageForwardRequest


class Messenger(ActorAbstract):
    def __init__(self, node_id: str, outbox: Outbox):
        self._node_id = node_id
        self._outbox = outbox

        self._address_cache = AddressCache()
        self._pending_messages: Dict[str, List[MessageForwardRequest]] = {}

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, MessageForwardRequest):
            self._forward_or_query_address(message)
        elif isinstance(message, QueryAddressResponse):
            self._query_address_response(message)
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
        self._outbox.send(Packet(message.message, sender=sender, receiver=receiver))

    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        if receiver_id == "discovery":
            packet = Packet(message,
                            sender=Address(self._node_id, sender_id),
                            receiver=Address("main", "discovery"))
        else:
            packet = Packet(MessageForwardRequest(message, sender_id, receiver_id),
                            sender=Address.on_local(sender_id),
                            receiver=Address.on_local("messenger"))
        self._outbox.send(packet)

    def _store_message(self, message: MessageForwardRequest, wait_for_address: str):
        self._pending_messages[wait_for_address] = self._pending_messages.get(wait_for_address, []) + [message]

    def _query_address_request(self, target: str):
        self.send(QueryAddressRequest(target, self._node_id, "messenger"), "", "discovery")

    def _query_address_response(self, response: QueryAddressResponse):
        for message in self._pending_messages.get(response.target, []):
            self._forward(message, Address(self._node_id, message.sender_id), response.address)
        self._pending_messages[response.target] = []
