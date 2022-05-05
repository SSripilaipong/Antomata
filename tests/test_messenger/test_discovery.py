from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.messenger import Messenger
from redcomet.messenger.address_cache import AddressCache
from redcomet.messenger.request import MessageForwardRequest
from tests.test_messenger.factory import create_messenger_with_node_id
from tests.test_messenger.mock import MockActorDiscoveryRef, DummyQueryAddressResponse, MockPacketHandler, DummyMessage, \
    MockQueue


def _start_parallel_inbox_process(messenger: Messenger):
    messenger.stop_receive_loop()
    messenger.start_receive_loop()
    messenger.close()


def test_should_forward_message_to_be_processed_later():
    inbox_queue = MockQueue()
    me = create_messenger_with_node_id("me", inbox_queue=inbox_queue)

    me.send(DummyMessage(123), "mine", "yours")

    expected = Packet(MessageForwardRequest(DummyMessage(123), "mine", "yours"),
                      sender=Address("me", "mine"), receiver=Address("me", "messenger"))
    assert inbox_queue.get() == expected


def test_should_send_query_message_to_discovery_when_address_is_unknown():
    discovery = MockActorDiscoveryRef()
    me = create_messenger_with_node_id("me")
    me.bind_discovery(discovery)
    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    assert discovery.queried_address == ("yours", "me", "messenger")


def test_should_forward_message_to_queried_address():
    your_handler = MockPacketHandler()
    me = create_messenger_with_node_id("me")
    you = create_messenger_with_node_id("you", handler=your_handler)
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", Address("you", "yours"))))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    _start_parallel_inbox_process(you)
    assert your_handler.received_packet.content.value == 123


def test_should_not_forward_message_when_queried_address_is_empty():
    your_handler = MockPacketHandler()
    my_handler = MockPacketHandler()
    me = create_messenger_with_node_id("me", handler=my_handler)
    you = create_messenger_with_node_id("you", handler=your_handler)
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", None)))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    _start_parallel_inbox_process(me)
    _start_parallel_inbox_process(you)
    assert your_handler.received_packet is None
    assert my_handler.received_packet is None


def test_should_cache_queried_address():
    cache = AddressCache()
    me = create_messenger_with_node_id("me", address_cache=cache)
    you = create_messenger_with_node_id("you")
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", Address("you", "yours"))))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    _start_parallel_inbox_process(you)
    assert cache.get_address("yours") == Address("you", "yours")


def test_should_use_cached_address_if_exists():
    cache = AddressCache()
    cache.update_cache(Address("you", "yours"))
    your_handler = MockPacketHandler()
    me = create_messenger_with_node_id("me", address_cache=cache)
    you = create_messenger_with_node_id("you", handler=your_handler)
    me.make_connection_to(you)

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    _start_parallel_inbox_process(you)

    assert your_handler.received_packet.content.value == 123
