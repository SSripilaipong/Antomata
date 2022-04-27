from redcomet.actor.executor import ActorExecutor
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.node.gateway import GatewayExecutor
from redcomet.node.synchronous import Node
from redcomet.queue.default import DefaultQueue


def create_gateway_node(node_id: str, incoming_messages: DefaultQueue) -> Node:
    return _create_node(node_id, GatewayExecutor(incoming_messages))


def create_worker_node(node_id: str) -> Node:
    return _create_node(node_id, ActorExecutor())


def _create_node(node_id: str, executor: ActorExecutor) -> Node:
    return Node.create(executor, Inbox(), Outbox(node_id))
