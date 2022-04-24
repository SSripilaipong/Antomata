from abc import ABC, abstractmethod

from redcomet.base.messaging.message import MessageAbstract


class InboxAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass
