from redcomet.base.actor.message import MessageAbstract


class MessageForwardRequest(MessageAbstract):
    def __init__(self, message: MessageAbstract, receiver_id: str):
        self._message = message
        self._receiver_id = receiver_id

    @property
    def message(self) -> MessageAbstract:
        return self._message

    @property
    def receiver_id(self) -> str:
        return self._receiver_id
