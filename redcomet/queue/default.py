from multiprocessing import Queue
from typing import Any

from redcomet.messenger.inbox.queue import QueueAbstract


class DefaultQueue(QueueAbstract):
    def __init__(self):
        self._queue = Queue()

    def put(self, obj, block: bool = True, timeout: float = None):
        self._queue.put(obj, block, timeout)

    def get(self, block: bool = True, timeout: float = None) -> Any:
        return self._queue.get(block, timeout)
