from typing import List

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.node.ref import NodeRef
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.queue.process_safe import ProcessSafeQueueManager
from redcomet.system.node_factory import create_gateway_node, create_worker_node


class ActorSystem:
    def __init__(self, cluster: ClusterManager, cluster_ref: ClusterRefAbstract, incoming_messages: QueueAbstract,
                 manager: ProcessSafeQueueManager):
        self._cluster = cluster
        self._cluster_ref = cluster_ref
        self._incoming_messages = incoming_messages
        self._manager = manager

    @classmethod
    def create(cls, n_worker_nodes: int = 1, node_id_prefix: str = "node", parallel: bool = False) -> 'ActorSystem':
        incoming_messages_manager = ProcessSafeQueueManager()
        incoming_messages = incoming_messages_manager.__enter__()

        gateway = create_gateway_node(incoming_messages, parallel=parallel)

        cluster = ClusterManager.create(gateway, "main", "cluster")
        for i in range(n_worker_nodes):
            cluster.add_node(create_worker_node(parallel=parallel), f"{node_id_prefix}{i}")

        return cls(cluster, gateway.issue_cluster_ref("main"), incoming_messages, incoming_messages_manager)

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        return self._cluster_ref.spawn(actor)

    def __enter__(self) -> 'ActorSystem':
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self._manager.__exit__(exc_type, exc_val, exc_tb)

    def fetch_message(self, timeout: float = None) -> MessageAbstract:
        return self._incoming_messages.get(timeout=timeout)

    def start(self):
        self._cluster.start()

    def stop(self):
        self._cluster.stop()

    def get_active_nodes(self, timeout: float) -> List[NodeRef]:
        return self._cluster_ref.get_active_nodes(timeout=timeout)
