from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.messaging.inbox import InboxAbstract
from redcomet.base.messaging.message import MessageAbstract


class Inbox(InboxAbstract):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract = None):
        self._node_id = node_id
        self._executor = executor

    def set_executor(self, executor: ActorExecutorAbstract):
        self._executor = executor

    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        local_receiver_id = receiver_id.split(".")[1]
        self._executor.execute(message, sender_id, local_receiver_id)
