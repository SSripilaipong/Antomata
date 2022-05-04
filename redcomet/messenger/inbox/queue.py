from abc import ABC, abstractmethod
from typing import Any


class QueueAbstract(ABC):
    @abstractmethod
    def put(self, obj: Any, block: bool = True, timeout: float = None):
        pass

    @abstractmethod
    def get(self, block: bool = True, timeout: float = None) -> Any:
        pass


class QueueManagerAbstract(ABC):

    @abstractmethod
    def start(self) -> QueueAbstract:
        pass

    @abstractmethod
    def shutdown(self):
        pass

    def __enter__(self) -> QueueAbstract:
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
