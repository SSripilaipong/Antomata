from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract


class ClusterRefAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        pass
