from abc import abstractmethod, ABC

from redcomet.base.actor.abstract import ActorAbstract


class NodeRefAbstract(ABC):
    @abstractmethod
    def register_address(self, actor_id: str, actor: ActorAbstract):
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass
