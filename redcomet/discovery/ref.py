from typing import Callable, Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.discovery.message.query.request import QueryAddressRequest
from redcomet.discovery.message.query.response import QueryAddressResponse
from redcomet.discovery.message.register.request import RegisterAddressRequest


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
                        sender=Address.on_local(requester_target),
                        receiver=self._address)
        self._messenger.send_packet(packet)

    def call_on_query_address_response(self, message: MessageAbstract, func: Callable[[str, Address], Any]) -> bool:
        if isinstance(message, QueryAddressResponse):
            func(message.target, message.address)
            return True
        return False

    def __eq__(self, other) -> bool:
        if other.__class__ != self.__class__:
            return False
        assert isinstance(other, ActorDiscoveryRef)
        return (self._messenger is other._messenger
                and self._address == other._address
                and self._issuer_id == other._issuer_id)
