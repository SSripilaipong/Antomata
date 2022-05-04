from redcomet.base.node.abstract import NodeAbstract
from redcomet.node.factory import create_node
from redcomet.node.gateway import GatewayActor
from redcomet.node.synchronous import SynchronousNode
from redcomet.queue.default import DefaultQueue


def create_gateway_node(incoming_messages: DefaultQueue, parallel: bool = False) -> SynchronousNode:
    node = create_node(parallel=parallel)
    node.register_executable_actor(GatewayActor(incoming_messages), actor_id="main")
    return node


def create_worker_node(parallel: bool = False) -> NodeAbstract:
    return create_node(parallel=parallel)
