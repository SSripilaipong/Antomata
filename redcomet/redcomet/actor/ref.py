from typing import Union

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, messenger: MessengerAbstract, local_issuer_id: str, ref_id: Union[str, Address]):
        self._messenger = messenger
        self._local_issuer_id = local_issuer_id
        self._ref_id = ref_id

    def bind(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._messenger, ref._local_issuer_id, self._ref_id)

    def tell(self, message: MessageAbstract):
        if isinstance(self._ref_id, Address):
            packet = Packet(message, sender=Address.on_local(self._local_issuer_id), receiver=self._ref_id)
            self._messenger.send_packet(packet)
        else:
            self._messenger.send(message, self._local_issuer_id, self.ref_id)

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __repr__(self) -> str:
        return f"ActorRef(..., local_issuer_id={self._local_issuer_id!r}, ref_id={self._ref_id!r})"
