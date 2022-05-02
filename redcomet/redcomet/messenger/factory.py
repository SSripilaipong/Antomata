from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.messenger import Messenger
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox


def create_messenger(handler: PacketHandlerAbstract, *, actor_id: str = "messenger", node_id: str = None) \
        -> MessengerAbstract:
    inbox = Inbox(handler)
    outbox = Outbox(node_id)
    outbox.register_inbox(inbox, node_id)
    return Messenger(actor_id, inbox, outbox, node_id=node_id)
