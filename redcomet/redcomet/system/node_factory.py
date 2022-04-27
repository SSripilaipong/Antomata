from redcomet.actor.executor import ActorExecutor
from redcomet.base.discovery import ActorDiscovery
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.messenger import Messenger
from redcomet.node.gateway import GatewayExecutor
from redcomet.node.synchronous import Node
from redcomet.queue.default import DefaultQueue


def create_gateway_node(node_id: str, incoming_messages: DefaultQueue, discovery: ActorDiscovery) \
        -> (Node, Inbox, Outbox, Messenger):
    node, inbox, outbox, messenger = _create_node(node_id, GatewayExecutor(incoming_messages), discovery)
    node.register_executable_actor(discovery, discovery.address.target)
    return node, inbox, outbox, messenger


def create_worker_node(node_id: str, discovery: ActorDiscovery) -> (Node, Inbox, Outbox):
    executor = ActorExecutor()
    node, inbox, outbox, _ = _create_node(node_id, executor, discovery)
    return node, inbox, outbox


def _create_node(node_id: str, executor: ActorExecutor, discovery: ActorDiscovery) -> (Node, Inbox, Outbox, Messenger):
    inbox = Inbox(node_id)
    outbox = Outbox(node_id)
    messenger = Messenger("messenger", node_id, outbox, discovery.address)

    node = Node.create(node_id, executor, messenger, inbox, discovery)

    return node, inbox, outbox, messenger
