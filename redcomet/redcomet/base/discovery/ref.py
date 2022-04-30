from abc import ABC, abstractmethod


class ActorDiscoveryRefAbstract(ABC):

    @abstractmethod
    def register_address(self, target: str, node_id: str):
        pass

    @abstractmethod
    def query_address(self, target: str, requester_node_id: str, requester_target: str):
        pass
