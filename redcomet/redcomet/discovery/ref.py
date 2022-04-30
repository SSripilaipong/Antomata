from typing import Callable, Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.query import QueryAddressRequest, QueryAddressResponse
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract


class ActorDiscoveryRef(ActorDiscoveryRefAbstract):
    def __init__(self, messenger: MessengerAbstract, address: Address, issuer_id: str):
        self._messenger = messenger
        self._address = address
        self._issuer_id = issuer_id

    def register_address(self, target: str, node_id: str):
        packet = Packet(RegisterAddressRequest(target, node_id),
                        sender=Address.on_local(self._issuer_id),
                        receiver=self._address)
        self._messenger.send_packet(packet)

    def query_address(self, target: str, requester_node_id: str, requester_target: str):
        packet = Packet(QueryAddressRequest(target, requester_node_id, requester_target),
                        sender=Address.on_local(""),
                        receiver=self._address)
        self._messenger.send_packet(packet)

    def call_on_query_address_response(self, message: MessageAbstract, func: Callable[[str, Address], Any]) -> bool:
        if isinstance(message, QueryAddressResponse):
            func(message.target, message.address)
            return True
        return False
