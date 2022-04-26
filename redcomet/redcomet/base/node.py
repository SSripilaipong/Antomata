from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract


class NodeAbstract(ABC):

    @abstractmethod
    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass
