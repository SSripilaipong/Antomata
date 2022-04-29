from multiprocessing.queues import Queue

from redcomet.base.actor.message import MessageAbstract


class ListActiveNodeRequest(MessageAbstract):
    def __init__(self, reply: Queue):
        self._reply = reply

    @property
    def reply(self) -> Queue:
        return self._reply
