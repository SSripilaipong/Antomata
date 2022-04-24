from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.node import NodeAbstract


class Cluster(ClusterAbstract):
    def __init__(self, node: NodeAbstract = None):
        self._node = node
        self._default_local_sender_id = None
        self._default_sender_node = None

    def set_node(self, node: NodeAbstract):
        self._node = node

    def set_default_sender_node(self, node: NodeAbstract):
        self._default_sender_node = node

    def set_default_local_sender_id(self, local_id: str):
        self._default_local_sender_id = local_id

    def spawn(self, actor: ActorAbstract, sender_node: NodeAbstract = None, local_sender_id: str = None) \
            -> ActorRefAbstract:
        receiver_id = self._node.register(actor)
        local_sender_id = local_sender_id or self._default_local_sender_id
        return (sender_node or self._node).issue_actor_ref(local_sender_id, receiver_id)
