from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet


class Inbox:
    def __init__(self, node_id: str, handler: PacketHandlerAbstract = None):
        self._node_id = node_id
        self._handler = handler

    def set_handler(self, handler: PacketHandlerAbstract):
        self._handler = handler

    def receive(self, packet: Packet):
        self._handler.handle(packet)
