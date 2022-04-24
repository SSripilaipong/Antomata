from typing import List, Tuple

from redcomet.actor.ref import ActorRef
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.cluster import Cluster
from redcomet.executor import Executor
from redcomet.inbox import Inbox
from redcomet.node.gateway import GatewayNode
from redcomet.node.synchronous import Node
from redcomet.outbox import Outbox
from redcomet.queue.default import DefaultQueue


class ActorSystem:
    def __init__(self):
        self._incoming_messages = DefaultQueue()

        self._cluster = Cluster()

        self._gateway, gateway_inbox, gateway_outbox = _create_gateway_node("main", self._incoming_messages)
        self._node, inbox0, outbox0 = _create_worker_node("node0", self._cluster)
        self._cluster.set_node(self._node)

        _wire_outboxes_to_inboxes([("main", gateway_inbox), ("node0", inbox0)], [gateway_outbox, outbox0])

    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return self._cluster.spawn(actor, self._gateway, "main")

    def __enter__(self) -> 'ActorSystem':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetch_message(self, timeout: float = None) -> MessageAbstract:
        return self._incoming_messages.get(timeout=timeout)


def _create_gateway_node(node_id: str, incoming_messages: DefaultQueue) -> (GatewayNode, Inbox, Outbox):
    inbox = Inbox(node_id)
    outbox = Outbox(node_id)

    return GatewayNode.create(node_id, outbox, inbox, incoming_messages), inbox, outbox


def _create_worker_node(node_id: str, cluster: Cluster) -> (Node, Inbox, Outbox):
    executor = Executor(node_id)
    inbox = Inbox(node_id)
    outbox = Outbox(node_id)

    executor.set_cluster(cluster)

    return Node.create(node_id, executor, outbox, inbox), inbox, outbox


def _wire_outboxes_to_inboxes(inboxes: List[Tuple[str, Inbox]], outboxes: List[Outbox]):
    for outbox in outboxes:
        for name, inbox in inboxes:
            outbox.register_inbox(inbox, name)
