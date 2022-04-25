from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.node import NodeAbstract


class ClusterRef(ClusterRefAbstract):
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
        ref_id = _generate_actor_id(actor)
        local_sender_id = local_sender_id or self._default_local_sender_id
        self._node.register(actor, ref_id)
        return (sender_node or self._node).issue_actor_ref(local_sender_id, ref_id)


def _generate_actor_id(actor: ActorAbstract) -> str:
    return str(id(actor))
