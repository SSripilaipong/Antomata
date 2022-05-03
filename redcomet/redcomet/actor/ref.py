from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, messenger: MessengerAbstract, local_issuer_id: str, address: Address):
        self._messenger = messenger
        self._local_issuer_id = local_issuer_id
        self._address = address

    def bind(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._messenger, ref._local_issuer_id, self._address)

    def tell(self, message: MessageAbstract):
        if self._address.is_global():
            self._messenger.send(message, self._local_issuer_id, self._address.target)
        else:
            packet = Packet(message, sender=Address.on_local(self._local_issuer_id), receiver=self._address)
            self._messenger.send_packet(packet)

    @property
    def address(self) -> Address:
        return self._address

    def __repr__(self) -> str:
        return f"ActorRef(..., local_issuer_id={self._local_issuer_id!r}, address={self._address!r})"
