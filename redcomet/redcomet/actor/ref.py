from redcomet.base.actor import ActorRefAbstract
from redcomet.base.messaging.message import MessageAbstract
from redcomet.base.messaging.outbox import OutboxAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, outbox: OutboxAbstract, local_issuer_id: str, ref_id: str):
        self._outbox = outbox
        self._local_issuer_id = local_issuer_id
        self._ref_id = ref_id

    def bind(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._outbox, ref._local_issuer_id, self._ref_id)

    def tell(self, message: MessageAbstract):
        self._outbox.send(message, self._local_issuer_id, self._ref_id)

    def __repr__(self) -> str:
        return f"ActorRef(..., local_issuer_id={self._local_issuer_id!r}, ref_id={self._ref_id!r})"
