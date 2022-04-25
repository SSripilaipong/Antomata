from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import PacketAbstract


class PacketHandlerAbstract(ABC):

    @abstractmethod
    def handle(self, packet: PacketAbstract, sender_id: str, receiver_id: str):
        pass
