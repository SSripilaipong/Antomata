from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.actor.ref import ActorRefAbstract

if TYPE_CHECKING:
    from redcomet.base.cluster.abstract import ClusterAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: 'ClusterAbstract'):
        pass
