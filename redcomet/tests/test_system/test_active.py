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
