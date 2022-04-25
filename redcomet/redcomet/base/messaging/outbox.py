from typing import Dict

from redcomet.base.actor.discovery import ActorDiscovery
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.packet import Packet


class Outbox:
    def __init__(self, node_id: str, discovery: ActorDiscovery):
        self._node_id = node_id
        self._discovery = discovery
        self._inboxes: Dict[str, Inbox] = {}

    def send(self, packet: Packet):
        packet.set_sender_node_id(self._node_id)
        packet.set_receiver_node_id(self._find_node_id(packet.receiver.target))
        self._find_inbox(packet.receiver.node_id).receive(packet)

    def _find_inbox(self, node_id: str) -> Inbox:
        inbox = self._inboxes.get(node_id)
        if inbox is None:
            raise NotImplementedError()
        return inbox

    def register_inbox(self, inbox: Inbox, node_id: str):
        if node_id in self._inboxes:
            raise NotImplementedError()
        self._inboxes[node_id] = inbox

    def _find_node_id(self, target: str) -> str:
        return self._discovery.query_node_id(target)
