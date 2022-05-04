from multiprocessing import Manager, Queue
from typing import Any

from redcomet.messenger.inbox.queue import QueueManagerAbstract, QueueAbstract


class ProcessSafeQueueManager(QueueManagerAbstract):
    def __init__(self):
        self._manager = None
        self._queue = None

    def start(self) -> QueueAbstract:
        self._manager = Manager()
        self._queue = self._manager.Queue()
        return ProcessSafeQueue(self._queue)

    def shutdown(self):
        self._manager.shutdown()


class ProcessSafeQueue(QueueAbstract):
    def __init__(self, queue: Queue):
        self._queue = queue

    def put(self, obj: Any, block: bool = True, timeout: float = None):
        self._queue.put(obj, block=block, timeout=timeout)

    def get(self, block: bool = True, timeout: float = None) -> Any:
        return self._queue.get(block=block, timeout=timeout)
