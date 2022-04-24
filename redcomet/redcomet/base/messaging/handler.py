from abc import ABC, abstractmethod

from redcomet.base.messaging.message import MessageAbstract


class MessageHandlerAbstract(ABC):

    @abstractmethod
    def handle(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass
