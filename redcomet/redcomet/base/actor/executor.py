from abc import ABC, abstractmethod

from redcomet.base.actor import ActorAbstract
from redcomet.base.actor.message import MessageAbstract


class ActorExecutorAbstract(ABC):

    @abstractmethod
    def register(self, local_id: str, actor: ActorAbstract):
        pass

    @abstractmethod
    def execute(self, message: MessageAbstract, sender_id: str, local_actor_id: str):
        pass
