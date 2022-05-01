from redcomet.base.messaging.address import Address
from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.factory import create_messenger


class DummyPacketContent(PacketContentAbstract):
    pass


class MockPacketHandler(PacketHandlerAbstract):

    def handle(self, packet: Packet):
        pass


def test_should_send_packet():
    sender = create_messenger("sender-node", MockPacketHandler())
    receiver = create_messenger("receiver-node", MockPacketHandler())
    sender.make_connection_to(receiver)

    sender.send_packet(Packet(DummyPacketContent(), Address.on_local("me"), Address("receiver-node", "you")))
