from redcomet.actor.executor import ActorExecutor
from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.discovery import ActorDiscovery
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messenger.messenger import Messenger
from redcomet.base.node import NodeAbstract
from redcomet.messaging.handler import PacketHandler


class Node(NodeAbstract):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract, messenger: Messenger, discovery: ActorDiscovery):
        self._node_id = node_id

        self._executor = executor
        self._messenger = messenger
        self._discovery = discovery

    @classmethod
    def create(cls, node_id: str, executor: ActorExecutor, messenger: Messenger, inbox: Inbox,
               discovery: ActorDiscovery) -> 'Node':
        node = cls(node_id, executor, messenger, discovery)
        executor.set_node(node)
        inbox.set_handler(PacketHandler(executor))
        node._executor.register("messenger", messenger)
        return node

    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        return ActorRef(self._messenger, local_issuer_id, ref_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    def register(self, actor: ActorAbstract, actor_id: str):
        self._executor.register(actor_id, actor)
        self._discovery.register(actor_id, self._node_id)
