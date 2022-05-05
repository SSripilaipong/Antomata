from pytest import raises

from redcomet.messenger.factory import create_messenger
from tests.test_messenger.mock import DummyMessage


def _create_messenger():
    return create_messenger(..., parallel=True)


def test_should_get_value_from_direct_message_box():
    messenger = _create_messenger()
    with messenger.create_direct_message_box() as box:
        box.put(DummyMessage("Hello"))
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


def test_should_put_message_with_ref_id_to_direct_message_box():
    messenger = _create_messenger()
    with messenger.create_direct_message_box() as box:
        messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


def test_should_ignore_message_when_ref_id_is_invalid():
    messenger = _create_messenger()
    messenger.receive(DummyMessage("Hello", ref_id="abc"), ..., ..., ...)


def test_should_ignore_operations_after_box_is_closed():
    messenger = _create_messenger()
    with messenger.create_direct_message_box() as box:
        pass
    messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
    assert box.get(timeout=0.1) is None


def test_should_raise_timeout_error():
    messenger = _create_messenger()
    with messenger.create_direct_message_box() as box:
        with raises(TimeoutError):
            box.get(timeout=0.0001)
