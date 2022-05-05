from pytest import raises

from tests.test_messenger.factory import create_messenger_for_test
from tests.test_messenger.mock import DummyMessage


def test_should_get_value_from_direct_message_box():
    messenger = create_messenger_for_test()
    with messenger.create_direct_message_box() as box:
        box.put(DummyMessage("Hello"))
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


def test_should_put_message_with_ref_id_to_direct_message_box():
    messenger = create_messenger_for_test()
    with messenger.create_direct_message_box() as box:
        messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


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
