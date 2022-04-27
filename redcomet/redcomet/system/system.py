from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.node import NodeAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system.node_factory import create_gateway_node, create_worker_node


class ActorSystem:
    def __init__(self, cluster: ClusterRefAbstract, gateway: NodeAbstract, incoming_messages: QueueAbstract):
        self._cluster = cluster
        self._gateway = gateway
        self._incoming_messages = incoming_messages

    @classmethod
    def create(cls) -> 'ActorSystem':
        incoming_messages = DefaultQueue()

        gateway = create_gateway_node("main", incoming_messages)

        node0 = create_worker_node("node0")

        cluster = ClusterManager.create(gateway, "cluster")
        cluster.add_node(node0, "node0")
        gateway.register_executable_actor(cluster, "cluster")

        return cls(gateway.issue_cluster_ref("main"), gateway, incoming_messages)

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
