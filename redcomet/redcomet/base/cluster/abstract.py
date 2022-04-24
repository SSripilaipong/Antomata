from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.node import NodeAbstract


class ClusterAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract, sender_node: NodeAbstract = None, local_sender_id: str = None) \
            -> ActorRefAbstract:
        pass
