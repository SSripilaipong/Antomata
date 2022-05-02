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
        ref_id = self._generate_ref_id()
        box = self._create_box(ref_id)
        return DirectMessageBoxRef(ref_id, box, self)

    def get_message_box(self, ref_id: str) -> DirectMessageBoxAbstract:
        with self._lock:
            box = self._boxes.get(ref_id, None)
        return box

    def destroy_message_box(self, ref_id: str):
        with self._lock:
            if ref_id in self._boxes:
                del self._boxes[ref_id]

    def _generate_ref_id(self) -> str:
        while True:
            ref_id = uuid.uuid4().hex
            with self._lock:
                if ref_id not in self._boxes:
                    return ref_id

    def _create_box(self, ref_id: str) -> Optional[DirectMessageBoxAbstract]:
        with self._lock:
            box = DirectMessageBox()
            self._boxes[ref_id] = box
        return box
