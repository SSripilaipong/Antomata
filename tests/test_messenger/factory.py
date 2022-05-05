from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.messenger.address_cache import AddressCache
from redcomet.messenger.factory import create_messenger
from redcomet.messenger.inbox.queue import QueueManagerAbstract, QueueAbstract
from tests.test_messenger.mock import MockPacketHandler, MockQueueManager, MockQueue


def create_messenger_for_test(node_id: str, handler: PacketHandlerAbstract = None,
                              inbox_queue_manager: QueueManagerAbstract = None,
                              inbox_queue: QueueAbstract = None, address_cache: AddressCache = None):
    handler = handler or MockPacketHandler()
    inbox_queue_manager = inbox_queue_manager or MockQueueManager()
    inbox_queue = inbox_queue or MockQueue()
    messenger = create_messenger(handler, inbox_queue_manager=inbox_queue_manager, inbox_queue=inbox_queue,
                                 address_cache=address_cache, parallel=True)
    messenger.assign_node_id(node_id)
    return messenger
