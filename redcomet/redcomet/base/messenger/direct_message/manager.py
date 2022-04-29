from abc import abstractmethod, ABC

from redcomet.base.messenger.direct_message.box import DirectMessageBoxAbstract


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
    def __init__(self, box: DirectMessageBoxAbstract, manager: DirectMessageManagerAbstract):
        self._box = box
        self._manager = manager

    def get(self, timeout: float):
        return self._box.get(timeout=timeout)

    @property
    def ref_id(self) -> str:
        return self._box.ref_id

    def __enter__(self) -> 'DirectMessageBoxRef':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._manager.destroy_message_box(self._box.ref_id)
