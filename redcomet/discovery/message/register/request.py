from redcomet.base.actor.message import MessageAbstract


class RegisterAddressRequest(MessageAbstract):
    def __init__(self, target: str, node_id: str):
        self._target = target
        self._node_id = node_id

    @property
    def target(self) -> str:
        return self._target

    @property
    def node_id(self) -> str:
        return self._node_id

    def __repr__(self) -> str:
        return f"RegisterAddressRequest({self._target!r}, {self._node_id!r})"
