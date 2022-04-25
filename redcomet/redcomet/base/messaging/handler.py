from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import Packet


class PacketHandlerAbstract(ABC):

    @abstractmethod
    def handle(self, packet: Packet, sender_id: str, receiver_id: str):
        pass
