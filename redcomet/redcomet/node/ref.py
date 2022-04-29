class NodeRef:
    def __init__(self, node_id: str):
        self._node_id = node_id

    def is_active(self, timeout: float) -> bool:
        return False

    @property
    def node_id(self) -> str:
        return self._node_id
