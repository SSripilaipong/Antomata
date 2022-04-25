from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import Packet


class InboxAbstract(ABC):

    @abstractmethod
    def receive(self, packet: Packet, sender_id: str, receiver_id: str):
        pass
