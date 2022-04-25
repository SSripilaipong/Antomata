from typing import List, Tuple

from redcomet.actor.executor import ActorExecutor
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.node import NodeAbstract
from redcomet.cluster import Cluster
from redcomet.messaging.inbox import Inbox
from redcomet.messaging.outbox import Outbox
from redcomet.node.gateway import GatewayNode
from redcomet.node.synchronous import Node
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue


class ActorSystem:
    def __init__(self, cluster: ClusterAbstract, gateway: NodeAbstract, incoming_messages: QueueAbstract):
        self._cluster = cluster
        self._gateway = gateway
        self._incoming_messages = incoming_messages

    @classmethod
    def create(cls) -> 'ActorSystem':
        incoming_messages = DefaultQueue()

        cluster = Cluster()

        gateway, gateway_inbox, gateway_outbox = _create_gateway_node("main", incoming_messages)
        node, inbox0, outbox0 = _create_worker_node("node0", cluster)
        cluster.set_node(node)

        _wire_outboxes_to_inboxes([("main", gateway_inbox), ("node0", inbox0)], [gateway_outbox, outbox0])
        return cls(cluster, gateway, incoming_messages)

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        return self._cluster.spawn(actor, self._gateway, "main")

    def __enter__(self) -> 'ActorSystem':
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def fetch_message(self, timeout: float = None) -> MessageAbstract:
        return self._incoming_messages.get(timeout=timeout)

    def start(self):
        pass

    def stop(self):
        pass


def _create_gateway_node(node_id: str, incoming_messages: DefaultQueue) -> (GatewayNode, Inbox, Outbox):
    inbox = Inbox(node_id)
    outbox = Outbox(node_id)

    return GatewayNode.create(node_id, outbox, inbox, incoming_messages), inbox, outbox


def _create_worker_node(node_id: str, cluster: Cluster) -> (Node, Inbox, Outbox):
    executor = ActorExecutor(node_id)
    inbox = Inbox(node_id)
    outbox = Outbox(node_id)

    executor.set_cluster(cluster)

    return Node.create(node_id, executor, outbox, inbox), inbox, outbox


def _wire_outboxes_to_inboxes(inboxes: List[Tuple[str, Inbox]], outboxes: List[Outbox]):
    for outbox in outboxes:
        for name, inbox in inboxes:
            outbox.register_inbox(inbox, name)
