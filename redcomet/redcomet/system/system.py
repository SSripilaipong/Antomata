from typing import List

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.node.ref import NodeRef
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system.node_factory import create_gateway_node, create_worker_node


class ActorSystem:
    def __init__(self, cluster: ClusterRefAbstract, incoming_messages: QueueAbstract):
        self._cluster = cluster
        self._incoming_messages = incoming_messages

    @classmethod
    def create(cls, n_worker_nodes: int = 1, node_id_prefix: str = "node") -> 'ActorSystem':
        incoming_messages = DefaultQueue()

        gateway = create_gateway_node(incoming_messages)

        cluster = ClusterManager.create(gateway, "main", "cluster")
        for i in range(n_worker_nodes):
            cluster.add_node(create_worker_node(), f"{node_id_prefix}{i}")

        return cls(gateway.issue_cluster_ref("main"), incoming_messages)

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        return self._cluster.spawn(actor)

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

    def get_active_nodes(self, timeout: float) -> List[NodeRef]:
        return self._cluster.get_active_nodes(timeout=timeout)
