from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.messenger import Messenger
from redcomet.messenger.address_cache import AddressCache
from redcomet.messenger.inbox import Inbox
from redcomet.messenger.outbox import Outbox


def create_messenger(handler: PacketHandlerAbstract, address_cache: AddressCache = None, *,
                     actor_id: str = "messenger") -> Messenger:
    return Messenger(actor_id, Inbox(handler), Outbox(), address_cache=address_cache)
