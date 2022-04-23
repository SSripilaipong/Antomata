from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.message.abstract import MessageAbstract
from redcomet.cluster import Cluster
from redcomet.executor import Executor
from redcomet.inbox import Inbox
from redcomet.node import Node
from redcomet.outbox import Outbox


class DummyActor(ActorAbstract):  # TODO: make use of this

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterAbstract):
        pass


class ActorSystem:
    def __init__(self, node_id: str = None):
        self._node_id = node_id or "main"
        outbox = Outbox(self._node_id)
        inbox = Inbox(self._node_id)
        executor = Executor(self._node_id)

        self._cluster = Cluster()
        self._node = Node(self._node_id, executor, outbox, inbox)

        outbox.set_node(self._node)
        inbox.set_node(self._node)
        executor.set_node(self._node)
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
