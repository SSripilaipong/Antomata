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


def _create_messenger_with_node_id(handler: PacketHandlerAbstract, node_id: str, parallel: bool = False):
    messenger = create_messenger(handler, parallel=parallel)
    messenger.assign_node_id(node_id)
    return messenger


def test_should_send_packet():
    sender = _create_messenger_with_node_id(MockPacketHandler(), "sender-node", parallel=True)
    receiver = _create_messenger_with_node_id(MockPacketHandler(), "receiver-node", parallel=True)
    sender.make_connection_to(receiver)

    sender.send_packet(Packet(DummyPacketContent(), Address.on_local("me"), Address("receiver-node", "you")))


def test_should_receive_packet():
    receiver_handler = MockPacketHandler()
    sender = _create_messenger_with_node_id(MockPacketHandler(), "sender-node", parallel=True)
    receiver = _create_messenger_with_node_id(receiver_handler, "receiver-node", parallel=True)
    sender.make_connection_to(receiver)

    sender.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address("receiver-node", "you")))
    receiver.stop()  # send stop message

    receiver.start_receive_loop()
    content: DummyPacketContent = receiver_handler.received_packet.content
    assert content.value == 123


def test_should_send_and_receive_packet_on_local_messenger():
    handler = MockPacketHandler()
    messenger = _create_messenger_with_node_id(handler, "node")

    messenger.send_packet(Packet(DummyPacketContent(123), Address.on_local("me"), Address.on_local("me-again")))
    content: DummyPacketContent = handler.received_packet.content
    assert content.value == 123
