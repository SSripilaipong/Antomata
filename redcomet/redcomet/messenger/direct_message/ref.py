from typing import Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.messenger.direct_message.box import DirectMessageBox
from redcomet.messenger.direct_message.manager import DirectMessageManager


class DirectMessageBoxRef(DirectMessageBoxRefAbstract):
    def __init__(self, ref_id: str, box: DirectMessageBox, manager: DirectMessageManager):
        self._ref_id = ref_id
        self._box = box
        self._manager = manager

    def put(self, item: MessageAbstract):
        if self._box is not None:
            self._box.put(item)

    def get(self, timeout: float) -> Any:
        if self._box is not None:
            return self._box.get(timeout=timeout)

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __enter__(self) -> 'DirectMessageBoxRef':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._box = None
        self._manager.destroy_message_box(self._ref_id)
