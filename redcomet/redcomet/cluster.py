from redcomet.actor.ref import ActorRef
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.node import NodeAbstract


class Cluster(ClusterAbstract):
    def __init__(self, node: NodeAbstract = None):
        self._node = node
        self._running_actor_local_id = None

    def set_node(self, node: NodeAbstract):
        self._node = node

    def set_running_actor_local_id(self, local_id: str):
        self._running_actor_local_id = local_id

    def spawn(self, actor: ActorAbstract) -> ActorRef:
        receiver_id = self._node.register(actor)
        return ActorRef.create(self._node, self._running_actor_local_id, receiver_id)
