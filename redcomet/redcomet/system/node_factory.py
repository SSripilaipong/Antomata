from redcomet.actor.executor import ActorExecutor
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox
from redcomet.node.gateway import GatewayExecutor
from redcomet.node.synchronous import Node
from redcomet.queue.default import DefaultQueue


def create_gateway_node(incoming_messages: DefaultQueue) -> Node:
    return _create_node(GatewayExecutor(incoming_messages))


def create_worker_node() -> Node:
    return _create_node(ActorExecutor())


def _create_node(executor: ActorExecutor) -> Node:
    return Node.create(executor, Inbox(), Outbox())
