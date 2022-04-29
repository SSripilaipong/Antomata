from typing import List, Optional

from redcomet.base.actor.message import MessageAbstract


class ListActiveNodeResponse(MessageAbstract):
    def __init__(self, node_ids: List[str]):
        self._node_ids = node_ids

    @property
    def node_ids(self) -> List[str]:
        return self._node_ids
