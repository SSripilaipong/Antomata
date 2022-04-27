from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery import ActorDiscovery
from redcomet.base.node import NodeAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.cluster.ref import ClusterRef
from redcomet.messenger import Messenger
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system.node_factory import create_gateway_node, create_worker_node


class ActorSystem:
    def __init__(self, cluster: ClusterRefAbstract, gateway: NodeAbstract, incoming_messages: QueueAbstract,
                 gateway_messenger: Messenger):
        self._cluster = cluster
        self._gateway = gateway
        self._incoming_messages = incoming_messages
        self._gateway_messenger = gateway_messenger

    @classmethod
    def create(cls) -> 'ActorSystem':
        incoming_messages = DefaultQueue()

        discovery = ActorDiscovery.create("discovery", "main")

        gateway, gateway_inbox, gateway_outbox, gateway_messenger \
            = create_gateway_node("main", incoming_messages, discovery)
        discovery.set_outbox(gateway_outbox)

        node0, inbox0, outbox0 = create_worker_node("node0", discovery)

        cluster = ClusterManager(gateway, gateway_messenger, "cluster")
        cluster.add_node(node0, "node0")
        gateway.register_executable_actor(cluster, "cluster")
        discovery.register_address("cluster", "main")

        return cls(ClusterRef(gateway_messenger, "main"), gateway, incoming_messages, gateway_messenger)

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
