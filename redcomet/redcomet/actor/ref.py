from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messaging.packet import Packet


class ActorRef(ActorRefAbstract):
    def __init__(self, outbox: Outbox, local_issuer_id: str, ref_id: str):
        self._outbox = outbox
        self._local_issuer_id = local_issuer_id
        self._ref_id = ref_id

    def bind(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._outbox, ref._local_issuer_id, self._ref_id)

    def tell(self, message: MessageAbstract):
        packet = Packet(message,
                        sender=Address.on_local(self._local_issuer_id),
                        receiver=Address(None, self._ref_id))
        self._outbox.send(packet)

    def __repr__(self) -> str:
        return f"ActorRef(..., local_issuer_id={self._local_issuer_id!r}, ref_id={self._ref_id!r})"
