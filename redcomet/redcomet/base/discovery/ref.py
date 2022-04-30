from abc import ABC, abstractmethod


class ActorDiscoveryRefAbstract(ABC):

    @abstractmethod
    def register_address(self, target: str, node_id: str):
        pass
