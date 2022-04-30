from typing import Dict, Optional

from redcomet.messenger.inbox import Inbox
from redcomet.base.messaging.packet import Packet


class Outbox:
    def __init__(self, node_id: str = None):
        self._node_id = node_id
        self._inboxes: Dict[str, Inbox] = {}

    def assign_node_id(self, node_id: str):
        if self._node_id is not None:
            if self._node_id != node_id:
                raise NotImplementedError()
        self._node_id = node_id

    def send(self, packet: Packet):
        packet.set_sender_node_id(self._node_id)
        self._find_inbox(packet.receiver.node_id).receive(packet)

    def _find_inbox(self, node_id: Optional[str]) -> Inbox:
        return self._inboxes.get(node_id or self._node_id)

    def register_inbox(self, inbox: Inbox, node_id: str):
        if node_id in self._inboxes:
            raise NotImplementedError()
        self._inboxes[node_id] = inbox
