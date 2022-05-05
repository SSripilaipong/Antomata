from queue import Queue
from typing import Any, Optional

from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet

from redcomet.messenger.inbox.queue import QueueAbstract, QueueManagerAbstract


class MockQueue(QueueAbstract):
    def __init__(self):
        self._queue = Queue()

    def put(self, obj: Any, block: bool = True, timeout: float = None):
        self._queue.put(obj)

    def get(self, block: bool = True, timeout: float = None) -> Any:
        return self._queue.get()


class MockQueueManager(QueueManagerAbstract):
    def start(self) -> QueueAbstract:
        pass

    def shutdown(self):
        pass


class MockPacketHandler(PacketHandlerAbstract):
    def __init__(self):
        self.received_packet: Optional[Packet] = None

    def handle(self, packet: Packet):
        self.received_packet = packet


class DummyPacketContent(PacketContentAbstract):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self) -> str:
        return f"DummyPacketContent({self.value!r})"

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, DummyPacketContent)
        return self.value == other.value
