from abc import ABC, abstractmethod


class QueueAbstract(ABC):
    @abstractmethod
    def put(self, obj, block=True, timeout=None):
        pass

    @abstractmethod
    def get(self, block: bool = True, timeout: float = None):
        pass
