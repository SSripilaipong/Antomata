from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import PacketAbstract


class OutboxAbstract(ABC):

    @abstractmethod
    def send(self, packet: PacketAbstract, local_id: str, receiver_id: str):
        pass
