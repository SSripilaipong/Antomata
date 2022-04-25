from typing import Dict


class ActorDiscovery:
    def __init__(self):
        self._mapper: Dict[str, str] = {}

    def register(self, actor_id: str, node_id: str):
        if actor_id in self._mapper:
            raise NotImplementedError()
        self._mapper[actor_id] = node_id

    def query_node_id(self, actor_id: str) -> str:
        node_id = self._mapper.get(actor_id)
        if node_id is None:
            raise NotImplementedError()
        return node_id
