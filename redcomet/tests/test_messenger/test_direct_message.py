from redcomet.base.actor.message import MessageAbstract
from redcomet.messenger.factory import create_messenger


class DummyMessage(MessageAbstract):
    def __init__(self, value, ref_id: str = None):
        self.value = value
        self._ref_id = ref_id

    @property
    def ref_id(self) -> str:
        return self._ref_id


def test_should_get_value_from_direct_message_box():
    messenger = create_messenger(...)
    with messenger.create_direct_message_box() as box:
        box.put(DummyMessage("Hello"))
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


def test_should_put_message_with_ref_id_to_direct_message_box():
    messenger = create_messenger(...)
    with messenger.create_direct_message_box() as box:
        messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"


def test_should_ignore_message_when_ref_id_is_invalid():
    messenger = create_messenger(...)
    messenger.receive(DummyMessage("Hello", ref_id="abc"), ..., ..., ...)


def test_should_ignore_operations_after_box_is_closed():
    messenger = create_messenger(...)
    with messenger.create_direct_message_box() as box:
        pass
    messenger.receive(DummyMessage("Hello", ref_id=box.ref_id), ..., ..., ...)
    assert box.get(timeout=0.1) is None
