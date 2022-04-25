from typing import Dict

from redcomet.base.messaging.inbox import InboxAbstract
from redcomet.base.messaging.outbox import OutboxAbstract
from redcomet.base.messaging.packet import Packet


class Outbox(OutboxAbstract):
    def __init__(self, node_id: str):
        self._node_id = node_id
        self._inboxes: Dict[str, InboxAbstract] = {}

    def send(self, packet: Packet):
        packet.set_sender_node_id(self._node_id)
        self._find_inbox(packet.receiver.to_str()).receive(packet)

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
