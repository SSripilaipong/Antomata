from redcomet.base.node.abstract import NodeAbstract
from redcomet.messenger.inbox.queue import QueueAbstract
from redcomet.node.factory import create_node
from redcomet.node.gateway import GatewayActor


def create_gateway_node(incoming_messages: QueueAbstract, parallel: bool = False) -> NodeAbstract:
    node = create_node(parallel=parallel)
    node.register_executable_actor(GatewayActor(incoming_messages), actor_id="main")
    return node


def create_worker_node(parallel: bool = False) -> NodeAbstract:
    return create_node(parallel=parallel)
