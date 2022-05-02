from queue import Queue

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messenger.direct_message.box import DirectMessageBoxAbstract


class DirectMessageBox(DirectMessageBoxAbstract):
    def __init__(self):
        self._queue = Queue()

    def get(self, timeout: float) -> MessageAbstract:
        return self._queue.get(timeout=timeout)

    def put(self, item: MessageAbstract):
        self._queue.put(item)
