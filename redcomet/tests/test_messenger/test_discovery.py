from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.factory import create_messenger
from redcomet.messenger.request import MessageForwardRequest


class DummyMessage(MessageAbstract):
    def __init__(self, value):
        self.value = value


class MockPacketHandler(PacketHandlerAbstract):
    def __init__(self):
        self.received_packet = None

    def handle(self, packet: Packet):
        self.received_packet = packet


def _create_messenger_with_node_id(handler: PacketHandlerAbstract, node_id: str):
    messenger = create_messenger(handler, actor_id="messenger")
    messenger.assign_node_id(node_id)
    return messenger


def test_should_forward_message_to_be_process_later():
    handler = MockPacketHandler()
    me = _create_messenger_with_node_id(handler, "me")

    me.send(DummyMessage(123), "mine", "yours")

    content = handler.received_packet.content
    assert isinstance(content, MessageForwardRequest) and content.message.value == 123
