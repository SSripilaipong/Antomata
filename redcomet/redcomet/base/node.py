from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract, ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messenger.messenger import MessengerAbstract


class NodeAbstract(ABC):

    @abstractmethod
    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        pass

    @abstractmethod
    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        pass

    @abstractmethod
    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass

    @property
    @abstractmethod
    def messenger(self) -> MessengerAbstract:
        pass
