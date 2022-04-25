from abc import ABC, abstractmethod

from redcomet.base.messaging.packet import PacketAbstract


class InboxAbstract(ABC):

    @abstractmethod
    def receive(self, packet: PacketAbstract, sender_id: str, receiver_id: str):
        pass
