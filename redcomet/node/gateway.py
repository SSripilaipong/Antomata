from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.messenger.inbox.queue import QueueAbstract


class GatewayActor(ActorAbstract):
    def __init__(self, queue: QueueAbstract):
        self._queue = queue

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        self._queue.put(message)
