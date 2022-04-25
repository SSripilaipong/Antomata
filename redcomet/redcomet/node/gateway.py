from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.actor.discovery import ActorDiscovery
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.messaging.handler import PacketHandler
from redcomet.node.synchronous import Node
from redcomet.queue.abstract import QueueAbstract


class GatewayNode(Node):
    def __init__(self, node_id: str, executor: ActorExecutorAbstract, outbox: Outbox,
                 incoming_queue: QueueAbstract, discovery: ActorDiscovery):
        super().__init__(node_id=node_id, executor=executor, outbox=outbox, discovery=discovery)

        self._incoming_queue = incoming_queue

    @classmethod
    def create(cls, node_id: str, outbox: Outbox, inbox: Inbox, incoming_queue: QueueAbstract,
               discovery: ActorDiscovery) -> 'GatewayNode':
        executor = EnqueueExecutor(incoming_queue)
        node = cls(node_id, executor, outbox, incoming_queue, discovery)
        inbox.set_handler(PacketHandler(executor))
        return node


class EnqueueExecutor(ActorExecutorAbstract):
    def __init__(self, queue: QueueAbstract):
        self._queue = queue

    def register(self, local_id: str, actor: ActorAbstract):
        pass

    def execute(self, message: MessageAbstract, sender: ActorRefAbstract, local_actor_id: str):
        self._queue.put(message)
