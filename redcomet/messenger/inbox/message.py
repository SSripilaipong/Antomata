from redcomet.base.messaging.content import PacketContentAbstract


class StopReceiveLoop(PacketContentAbstract):
    def __repr__(self) -> str:
        return "StopReceiveLoop()"
