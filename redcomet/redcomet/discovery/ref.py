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
