from typing import Optional

from redcomet.base.messaging.address import Address
from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.factory import create_messenger


class DummyPacketContent(PacketContentAbstract):
    def __init__(self, value=None):
        self.value = value


class MockPacketHandler(PacketHandlerAbstract):
    def __init__(self):
        self.received_packet: Optional[Packet] = None

    def handle(self, packet: Packet):
        self.received_packet = packet


def test_should_send_packet():
    sender = create_messenger(MockPacketHandler())
    receiver = create_messenger(MockPacketHandler())
    sender.assign_node_id("sender-node")
    receiver.assign_node_id("receiver-node")
    sender.make_connection_to(receiver)

    sender.send_packet(Packet(DummyPacketContent(), Address.on_local("me"), Address("receiver-node", "you")))


def test_should_receive_packet():
    receiver_handler = MockPacketHandler()
    sender = create_messenger(MockPacketHandler())
    receiver = create_messenger(receiver_handler)
    sender.assign_node_id("sender-node")
    receiver.assign_node_id("receiver-node")
    sender.make_connection_to(receiver)

    sender.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address("receiver-node", "you")))
    content: DummyPacketContent = receiver_handler.received_packet.content
    assert content.value == 123


def test_should_send_and_receive_packet_on_local_messenger():
    handler = MockPacketHandler()
    messenger = create_messenger(handler)
    messenger.assign_node_id("node")

    messenger.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address.on_local("me-again")))
    content: DummyPacketContent = handler.received_packet.content
    assert content.value == 123
