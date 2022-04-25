from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.outbox import OutboxAbstract
from redcomet.base.node import NodeAbstract
from redcomet.messaging.handler import PacketHandler
from redcomet.base.messaging.inbox import Inbox
from redcomet.messaging.outbox import Outbox
from redcomet.queue.abstract import QueueAbstract


class GatewayNode(NodeAbstract):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract, outbox: OutboxAbstract,
                 incoming_queue: QueueAbstract):
        self._node_id = node_id
        self._executor = executor
        self._outbox = outbox
        self._incoming_queue = incoming_queue

    @classmethod
    def create(cls, node_id: str, outbox: Outbox, inbox: Inbox, incoming_queue: QueueAbstract) -> 'GatewayNode':
        executor = EnqueueExecutor(incoming_queue)
        node = cls(node_id, executor, outbox, incoming_queue)
        inbox.set_handler(PacketHandler(executor))
        return node

    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        return ActorRef(self._outbox, local_issuer_id, ref_id)

    def make_global_id(self, local_id: str) -> str:
        return f"{self._node_id}.{local_id}"

    @property
    def node_id(self) -> str:
        return self._node_id

    def register(self, actor: ActorAbstract) -> str:
        raise NotImplementedError()


class EnqueueExecutor(ActorExecutorAbstract):
    def __init__(self, queue: QueueAbstract):
        self._queue = queue

    def register(self, local_id: str, actor: ActorAbstract):
        pass

    def execute(self, message: MessageAbstract, sender: ActorRefAbstract, local_actor_id: str):
        self._queue.put(message)
