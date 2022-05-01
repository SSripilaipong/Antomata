from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messenger.abstract import MessengerAbstract


def create_messenger(node_id: str, handler: PacketHandlerAbstract) -> MessengerAbstract:
    pass
