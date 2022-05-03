from abc import ABC, abstractmethod


class QueueAbstract(ABC):
    @abstractmethod
    def put(self, obj, block: bool = True, timeout: float = None):
        pass

    @abstractmethod
    def get(self, block: bool = True, timeout: float = None):
        pass
