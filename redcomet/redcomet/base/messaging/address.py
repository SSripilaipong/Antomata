from typing import Optional


class Address:
    def __init__(self, node_id: Optional[str], target: str):
        self._node_id = node_id
        self._target = target

    @classmethod
    def on_local(cls, target: str) -> 'Address':
        return cls(None, target)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def target(self) -> str:
        return self._target

    def set_node_id(self, node_id: str):
        self._node_id = node_id

    def to_str(self) -> str:
        assert self._node_id is not None
        return f"{self._node_id}.{self._target}"
