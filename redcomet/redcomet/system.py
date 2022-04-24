from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.cluster import Cluster
from redcomet.executor import Executor
from redcomet.inbox import Inbox
from redcomet.node.synchronous import Node
from redcomet.outbox import Outbox
from redcomet.queue.default import DefaultQueue


class DummyActor(ActorAbstract):  # TODO: make use of this

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterAbstract):
        pass


class ActorSystem:
    def __init__(self, node_id: str = None):
        self._node_id = node_id or "main"
        self._incoming_messages = DefaultQueue()
        executor = Executor(self._node_id)

        inbox = Inbox(self._node_id)

        outbox = Outbox(self._node_id)
        outbox.register_inbox(inbox, "main")

        self._node = Node.create(self._node_id, executor, outbox, inbox)
        self._cluster = Cluster()

        executor.set_cluster(self._cluster)
        self._cluster.set_node(self._node)

        global_id = self._node.register(DummyActor())
        _, self._my_id = global_id.split(".")
        self._ref = ActorRef.create(self._node, self._my_id, global_id)

    def spawn(self, actor: ActorAbstract) -> ActorRef:
        global_id = self._node.register(actor)
        return ActorRef.create(self._node, self._my_id, global_id)

    def __enter__(self) -> 'ActorSystem':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetch_message(self, timeout: float = None) -> MessageAbstract:
        pass
