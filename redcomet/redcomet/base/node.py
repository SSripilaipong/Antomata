from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.message.abstract import MessageAbstract


class NodeAbstract(ABC):

    @abstractmethod
    def send(self, message: MessageAbstract, local_id: str, receiver_id: str):
        pass

    @abstractmethod
    def make_global_id(self, local_id: str) -> str:
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass

    @abstractmethod
    def register(self, actor: ActorAbstract) -> str:
        pass
