from abc import ABC, abstractmethod

from redcomet.base.actor.message import MessageAbstract


class DirectMessageBoxAbstract(ABC):
    @abstractmethod
    def get(self, timeout: float) -> MessageAbstract:
        pass

    @abstractmethod
    def put(self, item: MessageAbstract):
        pass
