from redcomet.base.messaging.content import PacketContentAbstract


class StopReceiveLoop(PacketContentAbstract):
    def __repr__(self) -> str:
        return "StopReceiveLoop()"

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        return True
