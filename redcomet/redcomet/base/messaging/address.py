from typing import Optional


class Address:
    def __init__(self, node_id: Optional[str], actor_id: str):
        self._node_id = node_id
        self._actor_id = actor_id

    @classmethod
    def of_local(cls, actor_id: str) -> 'Address':
        return cls(None, actor_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def actor_id(self) -> str:
        return self._actor_id

    def set_node_id(self, node_id: str):
        self._node_id = node_id

    def to_str(self) -> str:
        assert self._node_id is not None
        return f"{self._node_id}.{self.actor_id}"
