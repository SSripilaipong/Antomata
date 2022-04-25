from abc import ABC, abstractmethod

from redcomet.base.actor.message import MessageAbstract


class ActorRefAbstract(ABC):

    @abstractmethod
    def tell(self, message: MessageAbstract):
        pass

    @abstractmethod
    def bind(self, ref: 'ActorRefAbstract') -> 'ActorRefAbstract':
        pass

    @property
    @abstractmethod
    def ref_id(self) -> str:
        pass
