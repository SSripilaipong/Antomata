from redcomet.actor.executor import ActorExecutor
from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.discovery import ActorDiscovery
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.node import NodeAbstract
from redcomet.messaging.handler import PacketHandler


class Node(NodeAbstract):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract, outbox: Outbox, discovery: ActorDiscovery):
        self._node_id = node_id

        self._outbox = outbox
        self._executor = executor
        self._discovery = discovery

    @classmethod
    def create(cls, node_id: str, executor: ActorExecutor, outbox: Outbox, inbox: Inbox, discovery: ActorDiscovery) \
            -> 'Node':
        node = cls(node_id, executor, outbox, discovery)
        executor.set_node(node)
        inbox.set_handler(PacketHandler(executor))
        return node

    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        return ActorRef(self._outbox, local_issuer_id, ref_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    def register(self, actor: ActorAbstract, actor_id: str):
        self._executor.register(actor_id, actor)
        self._discovery.register(actor_id, self._node_id)
