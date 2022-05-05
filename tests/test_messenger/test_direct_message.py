from pytest import raises

from redcomet.base.messaging.packet import Packet
from redcomet.messenger.inbox.message import StopReceiveLoop
from tests.test_messenger.factory import create_messenger_for_test
from tests.test_messenger.mock import DummyMessage, MockQueue


def test_should_put_message_to_direct_message_box():
    inbox_queue = MockQueue()
    messenger = create_messenger_for_test(inbox_queue=inbox_queue)
    with messenger.create_direct_message_box() as box:
        inbox_queue.put(Packet(DummyMessage("Hello", box.ref_id), sender=..., receiver=...))
        inbox_queue.put(Packet(StopReceiveLoop(), sender=..., receiver=...))
        messenger.start_receive_loop()

        assert box.get(timeout=0.1) == DummyMessage("Hello", box.ref_id)


def test_should_ignore_message_when_ref_id_is_invalid():
    messenger = create_messenger_for_test()
    messenger.receive(DummyMessage("Hello", ref_id="abc"), ..., ..., ...)


def test_should_ignore_operations_after_box_is_closed():
    messenger = create_messenger_for_test()
    with messenger.create_direct_message_box() as box:
        pass
    messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
    assert box.get(timeout=0.1) is None


def test_should_raise_timeout_error():
    messenger = create_messenger_for_test()
    with messenger.create_direct_message_box() as box:
        with raises(TimeoutError):
            box.get(timeout=0.0001)
