from typing import Optional


class Address:
    def __init__(self, node_id: Optional[str], local_id: str):
        self._node_id = node_id
        self._local_id = local_id

    @classmethod
    def of_local(cls, local_id: str) -> 'Address':
        return cls(None, local_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def local_id(self) -> str:
        return self._local_id

    def set_node_id(self, node_id: str):
        self._node_id = node_id
