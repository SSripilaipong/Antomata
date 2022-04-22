from abc import ABC, abstractmethod

from redcomet.message.abstract import MessageAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract):
        pass
