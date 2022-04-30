from typing import Dict

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.node import NodeAbstract


class ActorExecutor:
    def __init__(self, node: NodeAbstract = None):
        self._node = node
        self._actor_map: Dict[str, ActorAbstract] = {}

    def set_node(self, node: NodeAbstract):
        self._node = node

    def register(self, local_id: str, actor: ActorAbstract):
        if local_id in self._actor_map:
            raise NotImplementedError()

        self._actor_map[local_id] = actor

    def execute(self, message: MessageAbstract, sender_id: str, local_actor_id: str):
        sender = self._node.issue_actor_ref(local_actor_id, sender_id)
        actor = self._actor_map.get(local_actor_id)
        if actor is None:
            actor = self._on_no_actor(message, sender_id, local_actor_id)
            if actor is None:
                return

        me = self._node.issue_actor_ref(local_actor_id, local_actor_id)
        cluster = self._node.issue_cluster_ref(local_actor_id)
        try:
            actor.receive(message, sender, me, cluster)
        except Exception:
            raise NotImplementedError()

    def _on_no_actor(self, message: MessageAbstract, sender_id: str, local_actor_id: str) -> ActorAbstract:
        raise NotImplementedError()
