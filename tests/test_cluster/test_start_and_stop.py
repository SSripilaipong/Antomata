from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.node.manager.abstract import NodeManagerAbstract
from redcomet.node.ref import NodeRef


class MockNode(NodeAbstract):
    def __init__(self):
        self.is_started = False
        self.is_stopped = False
        self.is_closed = False

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_stopped = True

    def close(self):
        self.is_closed = True

    def bind_discovery(self, address: Address):
        pass

    def issue_actor_ref(self, local_issuer_id: str, address: Address) -> ActorRefAbstract:
        pass

    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        pass

    def issue_node_ref(self, local_issuer_id: str, node_id: str) -> NodeRef:
        pass

    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        pass

    def assign_node_id(self, node_id: str):
        pass

    @property
    def node_id(self) -> str:
        pass

    @property
    def messenger(self) -> MessengerAbstract:
        pass

    def make_connection_to(self, node: 'NodeAbstract'):
        pass

    def assign_manager(self, manager: NodeManagerAbstract):
        pass


def test_should_start_worker_nodes():
    manager = ClusterManager(MockNode(), "cluster", Address("my", "discovery"))
    node0, node1 = MockNode(), MockNode()
    manager.add_node(node0, "node0")
    manager.add_node(node1, "node1")
    manager.start()
    assert node0.is_started and node1.is_started


def test_should_stop_worker_nodes():
    manager = ClusterManager(MockNode(), "cluster", Address("my", "discovery"))
    node0, node1 = MockNode(), MockNode()
    manager.add_node(node0, "node0")
    manager.add_node(node1, "node1")
    manager.start()
    manager.stop()
    assert node0.is_stopped and node1.is_stopped


def test_should_close_worker_nodes():
    manager = ClusterManager(MockNode(), "cluster", Address("my", "discovery"))
    node0, node1 = MockNode(), MockNode()
    manager.add_node(node0, "node0")
    manager.add_node(node1, "node1")
    manager.start()
    manager.stop()
    assert node0.is_closed and node1.is_closed
