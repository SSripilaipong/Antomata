import pytest

from redcomet.system import ActorSystem


@pytest.mark.integration
def test_should_create_system_with_one_worker_node():
    with ActorSystem.create(n_worker_nodes=1, node_id_prefix="local") as system:
        active_nodes = system.get_active_nodes(timeout=0.01)
    assert sorted(node.node_id for node in active_nodes) == ["local0"]
