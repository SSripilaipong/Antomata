from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.packet import PacketAbstract


class ActorMessagePacket(PacketAbstract):
    def __init__(self, message: MessageAbstract):
        self._message = message

    @property
    def message(self) -> MessageAbstract:
        return self._message
