from abc import ABC, abstractmethod

from redcomet.base.message.abstract import MessageAbstract


class OutboxAbstract(ABC):

    @abstractmethod
    def send(self, message: MessageAbstract, local_id: str, receiver_id: str):
        pass
