from redcomet.messenger.factory import create_messenger


def test_should_get_value_from_direct_message_box():
    messenger = create_messenger(...)
    with messenger.create_direct_message_box() as box:
        box.put("Hello")
        value = box.get(timeout=0.1)
    assert value == "Hello"
