from redcomet.node.factory import create_node
from redcomet.node.gateway import GatewayActor
from redcomet.node.synchronous import SynchronousNode
from redcomet.queue.default import DefaultQueue


def create_gateway_node(incoming_messages: DefaultQueue) -> SynchronousNode:
    node = create_node()
    node.register_executable_actor(GatewayActor(incoming_messages), actor_id="main")
    return node


def create_worker_node() -> SynchronousNode:
    return create_node()
