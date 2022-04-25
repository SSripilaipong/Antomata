from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import Packet


class OutboxAbstract(ABC):

    @abstractmethod
    def send(self, packet: Packet):
        pass
