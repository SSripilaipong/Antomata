from abc import abstractmethod, ABC
from typing import Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messenger.direct_message.box import DirectMessageBoxAbstract
from redcomet.messenger.direct_message.box import DirectMessageBox


class DirectMessageManagerAbstract(ABC):

    @abstractmethod
    def create_message_box(self) -> 'DirectMessageBoxRef':
        pass

    @abstractmethod
    def get_message_box(self, ref_id: str) -> DirectMessageBoxAbstract:
        pass

    @abstractmethod
    def destroy_message_box(self, ref_id: str):
        pass


class DirectMessageBoxRef:
    def __init__(self, box: DirectMessageBox):
        self._box = box

    def put(self, item: MessageAbstract):
        self._box.put(item)

    def get(self, timeout: float) -> Any:
        return self._box.get(timeout=timeout)

    @property
    def ref_id(self) -> str:
        return self._box.ref_id

    def __enter__(self) -> 'DirectMessageBoxRef':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return
