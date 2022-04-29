from redcomet.node.ref import NodeRef
from redcomet.system import ActorSystem


def test_should_return_active_node():
    with ActorSystem.create(n_worker_nodes=1) as system:
        active_nodes = system.get_active_nodes(timeout=0.5)
        assert len(active_nodes) == 1 and isinstance(active_nodes[0], NodeRef)


def test_should_return_active_node_id():
    with ActorSystem.create(n_worker_nodes=1, node_id_prefix="local") as system:
        active_nodes = system.get_active_nodes(timeout=0.5)
        assert len(active_nodes) == 1 and active_nodes[0].node_id == "local0"


def test_should_return_multiple_active_node_ids():
    with ActorSystem.create(n_worker_nodes=2, node_id_prefix="local") as system:
        active_nodes = system.get_active_nodes(timeout=0.5)
        assert len(active_nodes) == 2
        assert active_nodes[0].node_id == "local0"
        assert active_nodes[1].node_id == "local1"
