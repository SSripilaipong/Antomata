from redcomet.actor.executor import ActorExecutor
from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract, ActorAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery import ActorDiscovery
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messenger.messenger import MessengerAbstract
from redcomet.base.node import NodeAbstract
from redcomet.cluster.ref import ClusterRef
from redcomet.messaging.handler import PacketHandler
from redcomet.messenger import Messenger
from redcomet.node.manager import NodeManager


class Node(NodeAbstract):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract, inbox: Inbox, outbox: Outbox,
                 messenger: Messenger, discovery: Address):
        self._node_id = node_id
        self._inbox = inbox
        self._outbox = outbox

        self._executor = executor
        self._messenger = messenger
        self._discovery = discovery

    @classmethod
    def create(cls, node_id: str, executor: ActorExecutor, messenger: Messenger, inbox: Inbox, outbox: Outbox,
               discovery: ActorDiscovery) -> 'Node':
        node = cls(node_id, executor, inbox, outbox, messenger, discovery.address)
        executor.set_node(node)
        inbox.set_handler(PacketHandler(executor))
        node._executor.register(messenger.actor_id, messenger)
        manager = NodeManager("manager", node, discovery.address)
        executor.register("manager", manager)
        return node

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
        self.outbox.register_inbox(node.inbox, node.node_id)

    @property
    def outbox(self) -> Outbox:
        return self._outbox

    @property
    def inbox(self) -> Inbox:
        return self._inbox

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def messenger(self) -> MessengerAbstract:
        return self._messenger
