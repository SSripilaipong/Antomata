from abc import ABC, abstractmethod

from redcomet.base.actor import ActorAbstract
from redcomet.base.message.abstract import MessageAbstract


class InboxAbstract(ABC):
    @abstractmethod
    def register(self, local_id: str, actor: ActorAbstract):
        pass

    @abstractmethod
    def receive(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass
