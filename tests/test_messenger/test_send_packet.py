from queue import Queue
from typing import Optional, Any

from redcomet.base.messaging.address import Address
from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.factory import create_messenger
from redcomet.messenger.inbox.message import StopReceiveLoop
from redcomet.messenger.inbox.queue import QueueAbstract, QueueManagerAbstract


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


class MockPacketHandler(PacketHandlerAbstract):
    def __init__(self):
        self.received_packet: Optional[Packet] = None

    def handle(self, packet: Packet):
        self.received_packet = packet


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


def _create_messenger_with_node_id(node_id: str, handler: PacketHandlerAbstract = None,
                                   inbox_queue_manager: QueueManagerAbstract = None,
                                   inbox_queue: QueueAbstract = None):
    handler = handler or MockPacketHandler()
    inbox_queue_manager = inbox_queue_manager or MockQueueManager()
    inbox_queue = inbox_queue or MockQueue()
    messenger = create_messenger(handler, inbox_queue_manager=inbox_queue_manager, inbox_queue=inbox_queue,
                                 parallel=True)
    messenger.assign_node_id(node_id)
    return messenger


def test_should_send_packet_to_receiver_inbox_queue():
    receiver_inbox_queue = MockQueue()
    sender = _create_messenger_with_node_id("sender-node")
    receiver = _create_messenger_with_node_id("receiver-node", inbox_queue=receiver_inbox_queue)
    sender.make_connection_to(receiver)

    packet = Packet(DummyPacketContent(), Address.on_local("me"), Address("receiver-node", "you"))
    sender.send_packet(packet)
    assert receiver_inbox_queue.get() == packet


def test_should_receive_packet_until_StopReceiveLoop():
    receiver_handler = MockPacketHandler()
    receiver_inbox_queue = MockQueue()

    receiver_inbox_queue.put(Packet(DummyPacketContent(123), Address("sender", "me"), Address("receiver", "you")))
    receiver_inbox_queue.put(Packet(StopReceiveLoop(), ..., ...))

    receiver = _create_messenger_with_node_id("receiver", inbox_queue=receiver_inbox_queue, handler=receiver_handler)

    receiver.start_receive_loop()

    assert receiver_handler.received_packet == \
           Packet(DummyPacketContent(123), Address("sender", "me"), Address("receiver", "you"))


def test_should_stop_receive_loop_by_sending_StopReceiveLoop():
    receiver_inbox_queue = MockQueue()
    receiver = _create_messenger_with_node_id("", inbox_queue=receiver_inbox_queue)
    receiver.stop_receive_loop()
    assert receiver_inbox_queue.get() == Packet(StopReceiveLoop(), ..., ...)


def test_should_send_packet_to_its_own_inbox_queue():
    inbox_queue = MockQueue()
    messenger = _create_messenger_with_node_id("node", inbox_queue=inbox_queue)

    messenger.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address.on_local("me-again")))
    assert inbox_queue.get() == Packet(DummyPacketContent(123), Address("node", "me"), Address("node", "me-again"))
