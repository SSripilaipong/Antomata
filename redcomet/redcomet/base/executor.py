from abc import ABC, abstractmethod

from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract


class ExecutorAbstract(ABC):

    @abstractmethod
    def register(self, local_id: str, actor: ActorAbstract):
        pass

    @abstractmethod
    def execute(self, message: MessageAbstract, sender: ActorRefAbstract, local_actor_id: str):
        pass
