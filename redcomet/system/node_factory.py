from redcomet.node.factory import create_node
from redcomet.node.gateway import GatewayActor
from redcomet.node.synchronous import Node
from redcomet.queue.default import DefaultQueue


def create_gateway_node(incoming_messages: DefaultQueue) -> Node:
    node = create_node()
    node.register_executable_actor(GatewayActor(incoming_messages), actor_id="main")
    return node


def create_worker_node() -> Node:
    return create_node()
