from redcomet.base.actor.message import MessageAbstract
from redcomet.messenger.factory import create_messenger


class DummyMessage(MessageAbstract):
    def __init__(self, value):
        self.value = value


def test_should_get_value_from_direct_message_box():
    messenger = create_messenger(...)
    with messenger.create_direct_message_box() as box:
        box.put(DummyMessage("Hello"))
        message: DummyMessage = box.get(timeout=0.1)
    assert message.value == "Hello"
