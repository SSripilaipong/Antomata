from redcomet.actor.executor import ActorExecutor
from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.cluster.ref import ClusterRef
from redcomet.discovery.ref import ActorDiscoveryRef
from redcomet.messaging.handler import PacketHandler
from redcomet.messenger import Messenger
from redcomet.node.manager import NodeManager


class Node(NodeAbstract):
    def __init__(self, executor: ActorExecutor, messenger: Messenger, node_id: str = None, manager: NodeManager = None):
        self._node_id = node_id
        self._actor_id = node_id

        self._executor = executor
        self._messenger = messenger
        self._manager = manager

    @classmethod
    def create(cls, executor: ActorExecutor, inbox: Inbox, outbox: Outbox) -> 'Node':
        messenger = Messenger("messenger", inbox, outbox)
        node = cls(executor, messenger)

        executor.set_node(node)

        inbox.set_handler(PacketHandler(executor))

        manager = NodeManager("manager", node)
        node._manager = manager

        executor.register(messenger.actor_id, messenger)
        executor.register("manager", manager)

        return node

    def bind_discovery(self, address: Address):
        ref = ActorDiscoveryRef(self._messenger, address, self._actor_id)
        self._manager.bind_discovery(ref)
        self._messenger.bind_discovery(address, ref)

    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        self._executor.register(actor_id, actor)

    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        return ClusterRef(self._messenger, local_issuer_id)

    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        return ActorRef(self._messenger, local_issuer_id, ref_id)

    def make_connection_with(self, node: NodeAbstract):
        self.make_connection_to(node)
        node.make_connection_to(self)

    def make_connection_to(self, node: NodeAbstract):
        self._messenger.make_connection_to(node.messenger)

    def assign_node_id(self, node_id: str):
        if self._node_id is not None:
            if self._node_id != node_id:
                raise NotImplementedError()
        self._node_id = node_id
        self._actor_id = node_id
        self._messenger.assign_node_id(node_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def messenger(self) -> MessengerAbstract:
        return self._messenger
