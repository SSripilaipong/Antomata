from abc import ABC, abstractmethod
from typing import List

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.node.ref import NodeRef


class ClusterRefAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        pass

    @abstractmethod
    def get_active_nodes(self, timeout: float) -> List[NodeRef]:
        pass
