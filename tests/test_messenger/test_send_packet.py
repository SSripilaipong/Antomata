from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.inbox.message import StopReceiveLoop
from tests.test_messenger.factory import create_messenger_for_test
from tests.test_messenger.mock import MockQueue, MockActorExecutor, DummyPacketContent


def test_should_send_packet_to_receiver_inbox_queue():
    receiver_inbox_queue = MockQueue()
    sender = create_messenger_for_test("sender-node")
    receiver = create_messenger_for_test("receiver-node", inbox_queue=receiver_inbox_queue)
    sender.make_connection_to(receiver)

    packet = Packet(DummyPacketContent(), Address.on_local("me"), Address("receiver-node", "you"))
    sender.send_packet(packet)
    assert receiver_inbox_queue.get() == packet


def test_should_receive_packet_until_StopReceiveLoop():
    receiver_handler = MockActorExecutor()
    receiver_inbox_queue = MockQueue()

    receiver_inbox_queue.put(Packet(DummyPacketContent(123), Address("sender", "me"), Address("receiver", "you")))
    receiver_inbox_queue.put(Packet(StopReceiveLoop(), ..., ...))

    receiver = create_messenger_for_test("receiver", inbox_queue=receiver_inbox_queue, executor=receiver_handler)

    receiver.start_receive_loop()

    assert receiver_handler.received_message == (DummyPacketContent(123), Address("sender", "me"), "you")


def test_should_stop_receive_loop_by_sending_StopReceiveLoop():
    receiver_inbox_queue = MockQueue()
    receiver = create_messenger_for_test("", inbox_queue=receiver_inbox_queue)
    receiver.stop_receive_loop()
    assert receiver_inbox_queue.get() == Packet(StopReceiveLoop(), ..., ...)


def test_should_send_packet_to_its_own_inbox_queue():
    inbox_queue = MockQueue()
    messenger = create_messenger_for_test("node", inbox_queue=inbox_queue)

    messenger.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address.on_local("me-again")))
    assert inbox_queue.get() == Packet(DummyPacketContent(123), Address("node", "me"), Address("node", "me-again"))
