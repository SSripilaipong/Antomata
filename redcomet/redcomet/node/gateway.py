from typing import Optional

from redcomet.actor.executor import ActorExecutor
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.queue.abstract import QueueAbstract


class GatewayExecutor(ActorExecutor):
    def __init__(self, queue: QueueAbstract, node: NodeAbstract = None):
        super().__init__(node=node)

        self._queue = queue

    def _on_no_actor(self, message: MessageAbstract, sender_id: str, local_actor_id: str) -> Optional[ActorAbstract]:
        self._queue.put(message)
        return None
