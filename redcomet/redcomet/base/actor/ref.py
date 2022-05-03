from abc import ABC, abstractmethod

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address


class ActorRefAbstract(ABC):

    @abstractmethod
    def tell(self, message: MessageAbstract):
        pass

    @abstractmethod
    def bind(self, ref: 'ActorRefAbstract') -> 'ActorRefAbstract':
        pass

    @property
    @abstractmethod
    def address(self) -> Address:
        pass
