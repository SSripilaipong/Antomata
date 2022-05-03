from typing import List

from redcomet.base.actor.message import MessageAbstract


class ListActiveNodeResponse(MessageAbstract):
    def __init__(self, node_ids: List[str], ref_id: str):
        self._node_ids = node_ids
        self._ref_id = ref_id

    @property
    def node_ids(self) -> List[str]:
        return self._node_ids

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __repr__(self) -> str:
        return f"ListActiveNodeResponse(node_ids={self._node_ids!r}, ref_id={self._ref_id!r})"
