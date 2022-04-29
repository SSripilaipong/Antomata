from redcomet.system import ActorSystem


def test_should_return_active_node():
    with ActorSystem.create() as system:
        node0, = system.get_active_nodes(timeout=0.5)
        assert node0.is_active(timeout=0.5)
