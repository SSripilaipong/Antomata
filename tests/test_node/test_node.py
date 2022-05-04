from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.discovery.ref import ActorDiscoveryRef
from redcomet.node.manager.abstract import NodeManagerAbstract
from redcomet.node.process import ProcessNode


class MockMessenger(MessengerAbstract):
    def __init__(self):
        self.bound_discovery = None

    def bind_discovery(self, ref: ActorDiscoveryRefAbstract):
        self.bound_discovery = ref

    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass

    def send_packet(self, packet: Packet):
        pass

    def assign_node_id(self, node_id: str):
        pass

    def make_connection_to(self, other: 'MessengerAbstract'):
        pass

    def create_direct_message_box(self) -> DirectMessageBoxRefAbstract:
        pass

    @property
    def node_id(self) -> str:
        pass


class MockManager(NodeManagerAbstract):
    def __init__(self):
        self.bound_discovery = None

    def bind_discovery(self, discovery: ActorDiscoveryRefAbstract):
        self.bound_discovery = discovery


def _create_node(messenger: MessengerAbstract) -> NodeAbstract:
    return ProcessNode(messenger)


def test_should_bind_messenger_to_discovery_ref():
    messenger = MockMessenger()
    node = _create_node(messenger)
    node.assign_node_id("node")
    node.assign_manager(MockManager())
    node.bind_discovery(Address("my", "discovery"))
    assert messenger.bound_discovery == ActorDiscoveryRef(messenger, Address("my", "discovery"), "node")


def test_should_bind_manager_to_discovery_ref():
    manager = MockManager()
    messenger = MockMessenger()
    node = _create_node(messenger)
    node.assign_node_id("node")
    node.assign_manager(manager)
    node.bind_discovery(Address("my", "discovery"))
    assert manager.bound_discovery == ActorDiscoveryRef(messenger, Address("my", "discovery"), "node")
