from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract
from redcomet.base.executor import ExecutorAbstract
from redcomet.base.inbox import InboxAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.node import NodeAbstract
from redcomet.base.outbox import OutboxAbstract


class Node(NodeAbstract):
    def __init__(self, node_id: str, executor: ExecutorAbstract, outbox: OutboxAbstract, inbox: InboxAbstract):
        self._node_id = node_id

        self._inbox = inbox
        self._outbox = outbox
        self._executor = executor

    def send(self, message: MessageAbstract, local_id: str, receiver_id: str):
        self._outbox.send(message, local_id, receiver_id)

    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        local_actor_id = receiver_id.split(".")[1]
        sender = ActorRef.create(self, local_actor_id, sender_id)
        self._executor.execute(message, sender, local_actor_id)

    def make_global_id(self, local_id: str) -> str:
        return f"{self._node_id}.{local_id}"

    @property
    def node_id(self) -> str:
        return self._node_id

    def register(self, actor: ActorAbstract) -> str:
        local_id = str(id(actor))
        self._executor.register(local_id, actor)
        self._inbox.register(local_id, actor)
        global_id = self.make_global_id(local_id)
        return global_id
