from queue import Queue, Empty

from redcomet.base.actor.message import MessageAbstract


class DirectMessageBox:
    def __init__(self):
        self._queue = Queue()

    def get(self, timeout: float) -> MessageAbstract:
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            raise TimeoutError()

    def put(self, item: MessageAbstract):
        self._queue.put(item)
