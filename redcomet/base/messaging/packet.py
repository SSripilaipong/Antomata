from redcomet.base.messaging.address import Address
from redcomet.base.messaging.content import PacketContentAbstract


class Packet:
    def __init__(self, content: PacketContentAbstract, sender: Address, receiver: Address):
        self._content = content
        self._sender = sender
        self._receiver = receiver

    def set_sender_node_id(self, node_id: str):
        self._sender.set_node_id(node_id)

    @property
    def content(self) -> PacketContentAbstract:
        return self._content

    @property
    def sender(self) -> Address:
        return self._sender

    @property
    def receiver(self) -> Address:
        return self._receiver

    def __repr__(self):
        return f"Packet({self._content!r}, sender={self._sender!r}, receiver={self._receiver!r})"

    def __eq__(self, other) -> bool:
        if other.__class__ is not self.__class__:
            return False
        assert isinstance(other, Packet)
        return other.content == self.content and other.receiver == self.receiver and other.sender == self.sender

    def set_receiver_node_id(self, node_id: str):
        self.receiver.set_node_id(node_id)

    def is_local_receiver(self) -> bool:
        return self._receiver.is_local()

    def is_local_sender(self) -> bool:
        return self._sender.is_local()
