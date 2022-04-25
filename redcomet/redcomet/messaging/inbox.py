from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.inbox import InboxAbstract
from redcomet.base.messaging.packet import PacketAbstract


class Inbox(InboxAbstract):
    def __init__(self, node_id: str, handler: PacketHandlerAbstract = None):
        self._node_id = node_id
        self._handler = handler

    def set_handler(self, handler: PacketHandlerAbstract):
        self._handler = handler

    def receive(self, packet: PacketAbstract, sender_id: str, receiver_id: str):
        self._handler.handle(packet, sender_id, receiver_id)
