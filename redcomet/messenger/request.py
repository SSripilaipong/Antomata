from redcomet.base.actor.message import MessageAbstract


class MessageForwardRequest(MessageAbstract):
    def __init__(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        self._message = message
        self._sender_id = sender_id
        self._receiver_id = receiver_id

    @property
    def message(self) -> MessageAbstract:
        return self._message

    @property
    def sender_id(self) -> str:
        return self._sender_id

    @property
    def receiver_id(self) -> str:
        return self._receiver_id

    def __repr__(self) -> str:
        return f"MessageForwardRequest({self._message!r}, sender_id={self._sender_id!r}, " \
               f"receiver_id={self.receiver_id!r})"

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, MessageForwardRequest)
        return (self._message == other._message
                and self._sender_id == other._sender_id
                and self._receiver_id == other._receiver_id)
