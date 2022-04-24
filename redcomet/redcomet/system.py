from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
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

        inbox = Inbox("main")
        outbox = Outbox("main")

        executor0 = Executor("node0")
        inbox0 = Inbox("node0")
        outbox0 = Outbox("node0")

        outbox.register_inbox(inbox, "main")
        outbox.register_inbox(inbox0, "node0")
        outbox0.register_inbox(inbox, "main")
        outbox0.register_inbox(inbox0, "node0")

        self._gateway = GatewayNode.create("main", outbox, inbox, self._incoming_messages)
        self._node = Node.create("node0", executor0, outbox0, inbox0)

        self._cluster = Cluster()

        executor0.set_cluster(self._cluster)
        self._cluster.set_node(self._node)

    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return self._cluster.spawn(actor, self._gateway, "main")

    def __enter__(self) -> 'ActorSystem':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetch_message(self, timeout: float = None) -> MessageAbstract:
        return self._incoming_messages.get(timeout=timeout)
