from typing import Optional

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.discovery.ref import ActorDiscoveryRef
from redcomet.node.executor import ActorExecutorAbstract
from redcomet.node.manager.abstract import NodeManagerAbstract
from redcomet.node.process import ProcessNode


class MockMessenger(MessengerAbstract):
    def __init__(self):
        self.bound_discovery = None
        self.assigned_node_id = None
        self.made_connection = None

    def bind_discovery(self, ref: ActorDiscoveryRefAbstract):
        self.bound_discovery = ref

    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass

    def send_packet(self, packet: Packet):
        pass

    def assign_node_id(self, node_id: str):
        self.assigned_node_id = node_id

    def make_connection_to(self, other: 'MessengerAbstract'):
        self.made_connection = other

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


class MockExecutor(ActorExecutorAbstract):
    def __init__(self):
        self.registered_actor_id = None
        self.registered_actor = None

    def register(self, local_id: str, actor: ActorAbstract):
        self.registered_actor_id = local_id
        self.registered_actor = actor

    def execute(self, message: MessageAbstract, sender: Address, local_actor_id: str):
        pass


class MockActor(ActorAbstract):
    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        pass


def _create_node(messenger: MessengerAbstract, executor: Optional[ActorExecutorAbstract]) -> NodeAbstract:
    return ProcessNode(messenger, executor)


def test_should_bind_messenger_to_discovery_ref():
    messenger = MockMessenger()
    node = _create_node(messenger, None)
    node.assign_node_id("node")
    node.assign_manager(MockManager())
    node.bind_discovery(Address("my", "discovery"))
    assert messenger.bound_discovery == ActorDiscoveryRef(messenger, Address("my", "discovery"), "node")


def test_should_bind_manager_to_discovery_ref():
    manager = MockManager()
    messenger = MockMessenger()
    node = _create_node(messenger, None)
    node.assign_node_id("node")
    node.assign_manager(manager)
    node.bind_discovery(Address("my", "discovery"))
    assert manager.bound_discovery == ActorDiscoveryRef(messenger, Address("my", "discovery"), "node")


def test_should_assign_node_id_to_messenger():
    messenger = MockMessenger()
    node = _create_node(messenger, None)
    node.assign_node_id("node")
    assert messenger.assigned_node_id == "node"


def test_should_provide_node_id():
    node = _create_node(MockMessenger(), None)
    node.assign_node_id("node")
    assert node.node_id == "node"


def test_should_provide_messenger():
    messenger = MockMessenger()
    node = _create_node(messenger, None)
    assert node.messenger is messenger


def test_should_make_connection_to_another_messenger():
    my_messenger = MockMessenger()
    me = _create_node(my_messenger, None)
    your_messenger = MockMessenger()
    you = _create_node(your_messenger, None)

    me.make_connection_with(you)

    assert your_messenger.made_connection is my_messenger and my_messenger.made_connection is your_messenger


def test_should_register_actor_to_executor():
    executor = MockExecutor()
    actor = MockActor()
    node = _create_node(MockMessenger(), executor)
    node.register_executable_actor(actor, "my_actor")
    assert executor.registered_actor is actor and executor.registered_actor_id == "my_actor"
