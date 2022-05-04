from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract


class ActorExecutorAbstract(ABC):

    @abstractmethod
    def register(self, local_id: str, actor: ActorAbstract):
        pass
