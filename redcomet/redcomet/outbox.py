from typing import Dict

from redcomet.base.inbox import InboxAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.outbox import OutboxAbstract


class Outbox(OutboxAbstract):
    def __init__(self, node_id: str):
        self._node_id = node_id
        self._inboxes: Dict[str, InboxAbstract] = {}

    def send(self, message: MessageAbstract, local_id: str, receiver_id: str):
        sender_id = f'{self._node_id}.{local_id}'
        self._find_inbox(receiver_id).receive(message, sender_id, receiver_id)

    def _find_inbox(self, receiver_id: str) -> InboxAbstract:
        node_id = receiver_id.split(".")[0]
        inbox = self._inboxes.get(node_id)
        if inbox is None:
            raise NotImplementedError()
        return inbox

    def register_inbox(self, inbox: InboxAbstract, node_id: str):
        if node_id in self._inboxes:
            raise NotImplementedError()
        self._inboxes[node_id] = inbox
