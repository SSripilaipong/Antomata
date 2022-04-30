from abc import ABC, abstractmethod

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messaging.packet import Packet


class MessengerAbstract(ABC):

    @abstractmethod
    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass

    @abstractmethod
    def send_packet(self, packet: Packet):
        pass

    @abstractmethod
    def make_connection_to(self, other: 'MessengerAbstract'):
        pass

    @property
    @abstractmethod
    def inbox(self) -> Inbox:
        pass

    @property
    @abstractmethod
    def outbox(self) -> Outbox:
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass
