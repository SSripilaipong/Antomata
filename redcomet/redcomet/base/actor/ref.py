from abc import ABC, abstractmethod

from redcomet.base.messaging.message import MessageAbstract


class ActorRefAbstract(ABC):

    @abstractmethod
    def tell(self, message: MessageAbstract):
        pass

    @abstractmethod
    def bind(self, ref: 'ActorRefAbstract') -> 'ActorRefAbstract':
        pass
