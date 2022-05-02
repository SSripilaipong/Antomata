from redcomet.actor.executor import ActorExecutor
from redcomet.node.factory import create_node
from redcomet.node.gateway import GatewayExecutor
from redcomet.node.synchronous import Node
from redcomet.queue.default import DefaultQueue


def create_gateway_node(incoming_messages: DefaultQueue) -> Node:
    return create_node(GatewayExecutor(incoming_messages))


def create_worker_node() -> Node:
    return create_node(ActorExecutor())
