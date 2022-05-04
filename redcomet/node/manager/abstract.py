from abc import ABC, abstractmethod

from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract


class NodeManagerAbstract(ABC):
    @abstractmethod
    def bind_discovery(self, discovery: ActorDiscoveryRefAbstract):
        pass
