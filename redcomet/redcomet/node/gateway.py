from typing import Optional

from redcomet.actor.executor import ActorExecutor
from redcomet.base.actor import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.node import NodeAbstract
from redcomet.cluster.ref import ClusterRef
from redcomet.queue.abstract import QueueAbstract


class GatewayExecutor(ActorExecutor):
    def __init__(self, node_id: str, queue: QueueAbstract, node: NodeAbstract = None, cluster: ClusterRef = None):
        super().__init__(node_id=node_id, node=node, cluster=cluster)

        self._queue = queue

    def _on_no_actor(self, message: MessageAbstract, sender_id: str, local_actor_id: str) -> Optional[ActorAbstract]:
        self._queue.put(message)
        return None
