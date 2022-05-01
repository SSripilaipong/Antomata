from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.messenger import Messenger
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox


def create_messenger(handler: PacketHandlerAbstract, *, node_id: str = None) -> MessengerAbstract:
    return Messenger("messenger", Inbox(handler), Outbox(node_id), node_id=node_id)
