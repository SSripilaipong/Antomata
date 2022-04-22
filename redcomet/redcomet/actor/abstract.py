from abc import ABC, abstractmethod

from redcomet.message.abstract import MessageAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract):
        pass

    def handle_message(self, message: MessageAbstract):
        self.receive(message)
