from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import Packet


class PacketHandlerAbstract(ABC):

    @abstractmethod
    def handle(self, packet: Packet):
        pass
