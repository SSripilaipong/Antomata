from redcomet.base.messaging.handler import MessageHandlerAbstract
from redcomet.base.messaging.inbox import InboxAbstract
from redcomet.base.messaging.message import MessageAbstract


class Inbox(InboxAbstract):
    def __init__(self, node_id: str, handler: MessageHandlerAbstract = None):
        self._node_id = node_id
        self._handler = handler

    def set_handler(self, handler: MessageHandlerAbstract):
        self._handler = handler

    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        self._handler.handle(message, sender_id, receiver_id)
