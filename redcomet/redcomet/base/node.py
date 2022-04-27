from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract


class NodeAbstract(ABC):

    @abstractmethod
    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        pass

    @abstractmethod
    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass
