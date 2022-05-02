from abc import ABC, abstractmethod
from typing import Any

from redcomet.base.actor.message import MessageAbstract


class DirectMessageBoxRefAbstract(ABC):

    @abstractmethod
    def put(self, item: MessageAbstract):
        pass

    @abstractmethod
    def get(self, timeout: float) -> Any:
        pass

    @property
    @abstractmethod
    def ref_id(self) -> str:
        pass

    @abstractmethod
    def __enter__(self) -> 'DirectMessageBoxRefAbstract':
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
