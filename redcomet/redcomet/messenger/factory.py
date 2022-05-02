from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.messenger import Messenger
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox


def create_messenger(handler: PacketHandlerAbstract, *, actor_id: str = "messenger") \
        -> MessengerAbstract:
    return Messenger(actor_id, Inbox(handler), Outbox())
