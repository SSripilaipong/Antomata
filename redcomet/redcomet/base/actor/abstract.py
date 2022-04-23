from abc import ABC, abstractmethod

from redcomet.base.message.abstract import MessageAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract, sender: 'ActorRefAbstract', me: 'ActorRefAbstract'):
        pass


class ActorRefAbstract(ABC):

    @abstractmethod
    def tell(self, message: MessageAbstract):
        pass

    @classmethod
    @abstractmethod
    def of(cls, actor: ActorAbstract) -> 'ActorRefAbstract':
        pass
