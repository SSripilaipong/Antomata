from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract
from redcomet.base.executor import ExecutorAbstract
from redcomet.base.inbox import InboxAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.node import NodeAbstract


class Inbox(InboxAbstract):
    def __init__(self, node_id: str, node: NodeAbstract = None, executor: ExecutorAbstract = None):
        self._node_id = node_id
        self._node = node
        self._executor = executor

    def set_node(self, node: NodeAbstract):
        self._node = node

    def set_executor(self, executor: ExecutorAbstract):
        self._executor = executor

    def register(self, local_id: str, actor: ActorAbstract):
        pass

    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        local_receiver_id = receiver_id.split(".")[1]
        sender = ActorRef.create(self._node, local_receiver_id, sender_id)
        self._executor.execute(message, sender, local_receiver_id)
