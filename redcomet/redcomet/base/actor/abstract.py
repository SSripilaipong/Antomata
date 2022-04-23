from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from redcomet.base.actor.ref import ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract

if TYPE_CHECKING:
    from redcomet.base.cluster.abstract import ClusterAbstract


class ActorAbstract(ABC):

    @abstractmethod
    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: 'ClusterAbstract'):
        pass
