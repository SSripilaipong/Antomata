from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.actor.ref import ActorRefAbstract

if TYPE_CHECKING:
    from redcomet.base.cluster.ref import ClusterRefAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: 'ClusterRefAbstract'):
        pass
