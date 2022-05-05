from abc import ABC, abstractmethod

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.content import PacketContentAbstract


class ActorExecutorAbstract(ABC):

    @abstractmethod
    def register(self, local_id: str, actor: ActorAbstract):
        pass

    @abstractmethod
    def execute(self, message: PacketContentAbstract, sender: Address, local_actor_id: str):
        pass
