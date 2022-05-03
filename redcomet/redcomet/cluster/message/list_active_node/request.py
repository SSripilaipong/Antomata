from redcomet.base.actor.message import MessageAbstract


class ListActiveNodeRequest(MessageAbstract):
    def __init__(self, reply_ref_id: str):
        self._reply_ref_id = reply_ref_id

    @property
    def reply_ref_id(self) -> str:
        return self._reply_ref_id

    def __repr__(self) -> str:
        return f"ListActiveNodeRequest(reply_ref_id={self._reply_ref_id!r})"
