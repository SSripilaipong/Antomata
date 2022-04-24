from redcomet.base.actor import ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.node import NodeAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, local_node: NodeAbstract, local_id: str, receiver_id: str):
        self._local_node = local_node
        self._local_id = local_id
        self._receiver_id = receiver_id

    def for_actor(self, ref: 'ActorRef') -> 'ActorRef':
        return ActorRef(ref._local_node, ref._local_id, self._receiver_id)

    def tell(self, message: MessageAbstract):
        self._local_node.send(message, self._local_id, self._receiver_id)

    @classmethod
    def create(cls, local_node: NodeAbstract, local_id: str, receiver_id: str) -> 'ActorRef':
        return ActorRef(local_node, local_id, receiver_id)

    def __repr__(self) -> str:
        return f"ActorRef(..., local_id={self._local_id!r}, receiver_id={self._receiver_id!r})"
