from abc import ABC, abstractmethod

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.messenger.messenger import MessengerAbstract


class ClusterRefAbstract(ABC):
    @abstractmethod
    def spawn(self, actor: ActorAbstract, local_messenger: MessengerAbstract = None, local_sender_id: str = None) \
            -> ActorRefAbstract:
        pass
