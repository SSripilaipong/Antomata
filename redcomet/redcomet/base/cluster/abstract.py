from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor import ActorRefAbstract


class ClusterAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        pass
