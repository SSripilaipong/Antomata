from typing import Optional


class Address:
    def __init__(self, node_id: Optional[str], target: str):
        self._node_id = node_id
        self._target = target

    @classmethod
    def on_local(cls, target: str) -> 'Address':
        return cls("__LOCAL", target)

    @classmethod
    def anywhere(cls, target: str) -> 'Address':
        return cls("__ANYWHERE", target)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def target(self) -> str:
        return self._target

    def set_node_id(self, node_id: str):
        self._node_id = node_id

    def is_local(self) -> bool:
        return self._node_id == "__LOCAL"

    def is_global(self) -> bool:
        return self._node_id == "__ANYWHERE"

    def __repr__(self):
        return f"Address({self._node_id!r}, {self.target!r})"

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        assert isinstance(other, Address)
        return self._node_id == other._node_id and self._target == other.target
