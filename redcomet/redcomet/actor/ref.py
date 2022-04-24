from redcomet.base.actor import ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.outbox import OutboxAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, outbox: OutboxAbstract, local_id: str, receiver_id: str):
        self._outbox = outbox
        self._local_id = local_id
        self._receiver_id = receiver_id

    def bind(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._outbox, ref._local_id, self._receiver_id)

    def tell(self, message: MessageAbstract):
        self._outbox.send(message, self._local_id, self._receiver_id)

    def __repr__(self) -> str:
        return f"ActorRef(..., local_id={self._local_id!r}, receiver_id={self._receiver_id!r})"
