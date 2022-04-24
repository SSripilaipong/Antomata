from redcomet.base.executor import ExecutorAbstract
from redcomet.base.inbox import InboxAbstract
from redcomet.base.message.abstract import MessageAbstract


class Inbox(InboxAbstract):
    def __init__(self, node_id: str, executor: ExecutorAbstract = None):
        self._node_id = node_id
        self._executor = executor

    def set_executor(self, executor: ExecutorAbstract):
        self._executor = executor

    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        local_receiver_id = receiver_id.split(".")[1]
        self._executor.execute(message, sender_id, local_receiver_id)
