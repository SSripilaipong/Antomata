from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.message.abstract import MessageAbstract


class ActorRefAbstract(ABC):

    @abstractmethod
    def tell(self, message: MessageAbstract):
        pass

    @classmethod
    @abstractmethod
    def of(cls, actor: ActorAbstract) -> 'ActorRefAbstract':
        pass
