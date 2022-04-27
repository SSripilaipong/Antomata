from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet


class Inbox:
    def __init__(self, handler: PacketHandlerAbstract = None):
        self._handler = handler

    def set_handler(self, handler: PacketHandlerAbstract):
        self._handler = handler

    def receive(self, packet: Packet):
        self._handler.handle(packet)
