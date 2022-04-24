from redcomet.base.actor import ActorAbstract
from redcomet.base.executor import ExecutorAbstract
from redcomet.base.inbox import InboxAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.node import NodeAbstract
from redcomet.base.outbox import OutboxAbstract
from redcomet.executor import Executor
from redcomet.inbox import Inbox
from redcomet.outbox import Outbox


class Node(NodeAbstract):
    def __init__(self, node_id: str, executor: ExecutorAbstract, outbox: OutboxAbstract, inbox: InboxAbstract):
        self._node_id = node_id

        self._inbox = inbox
        self._outbox = outbox
        self._executor = executor

    @classmethod
    def create(cls, node_id: str, executor: Executor, outbox: Outbox, inbox: Inbox) -> 'Node':
        node = cls(node_id, executor, outbox, inbox)
        executor.set_node(node)
        inbox.set_node(node)
        inbox.set_executor(executor)
        return node

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
