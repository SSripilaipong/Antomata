import uuid
from threading import Lock
from typing import Dict, Optional

from redcomet.base.messenger.direct_message.box import DirectMessageBoxAbstract
from redcomet.base.messenger.direct_message.manager import DirectMessageManagerAbstract, DirectMessageBoxRef
from redcomet.messenger.direct_message.box import DirectMessageBox


class DirectMessageManager(DirectMessageManagerAbstract):
    def __init__(self):
        self._boxes: Dict[str, DirectMessageBoxAbstract] = {}
        self._lock = Lock()

    def create_message_box(self) -> DirectMessageBoxRef:
        box = self._create_box_with_ref_id()
        return DirectMessageBoxRef(box=box)

    def get_message_box(self, ref_id: str) -> DirectMessageBoxAbstract:
        with self._lock:
            box = self._boxes.get(ref_id, None)
        if box is None:
            raise KeyError("Direct message box with specified ref_id not found.")
        return box

    def destroy_message_box(self, ref_id: str):
        with self._lock:
            if ref_id in self._boxes:
                del self._boxes[ref_id]

    def _create_box_with_ref_id(self) -> DirectMessageBoxAbstract:
        while True:
            ref_id = uuid.uuid4().hex
            box = self._create_box(ref_id)
            if box is not None:
                return box

    def _create_box(self, ref_id: str) -> Optional[DirectMessageBoxAbstract]:
        with self._lock:
            if ref_id in self._boxes:
                return None
            box = DirectMessageBox(ref_id)
            self._boxes[ref_id] = box
        return box
