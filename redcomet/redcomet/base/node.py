from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract


class NodeAbstract(ABC):

    @abstractmethod
    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
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
