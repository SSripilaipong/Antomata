from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.ref import ActorRefAbstract


class ClusterAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        pass
