from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.address_cache import AddressCache
from redcomet.messenger.request import MessageForwardRequest
from tests.test_messenger.factory import create_messenger_for_test
from tests.test_messenger.mock import MockActorDiscoveryRef, DummyQueryAddressResponse, DummyMessage, MockQueue


def test_should_forward_message_to_be_processed_later():
    inbox_queue = MockQueue()
    me = create_messenger_for_test("me", inbox_queue=inbox_queue)

    me.send(DummyMessage(123), "mine", "yours")

    expected = Packet(MessageForwardRequest(DummyMessage(123), "mine", "yours"),
                      sender=Address("me", "mine"), receiver=Address("me", "messenger"))
    assert inbox_queue.get() == expected


def test_should_send_query_message_to_discovery_when_address_is_unknown():
    discovery = MockActorDiscoveryRef()
    me = create_messenger_for_test("me", discovery_ref=discovery)
    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    assert discovery.queried_address == ("yours", "me", "messenger")


def test_should_forward_message_to_queried_address_when_received_response():
    your_inbox_queue = MockQueue()
    me = create_messenger_for_test("me")
    you = create_messenger_for_test("you", inbox_queue=your_inbox_queue)
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", Address("you", "yours"))))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    expected = Packet(DummyMessage(123), sender=Address("me", "mine"), receiver=Address("you", "yours"))
    assert your_inbox_queue.get() == expected


def test_should_not_forward_message_when_queried_address_is_empty():
    my_inbox_queue, your_inbox_queue = MockQueue(), MockQueue()
    me = create_messenger_for_test("me", inbox_queue=my_inbox_queue)
    you = create_messenger_for_test("you", inbox_queue=your_inbox_queue)
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", None)))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    assert your_inbox_queue.empty() and my_inbox_queue.empty()


def test_should_cache_queried_address():
    cache = AddressCache()
    me = create_messenger_for_test("me", address_cache=cache)
    you = create_messenger_for_test("you")
    me.make_connection_to(you)
    me.bind_discovery(MockActorDiscoveryRef(query_response_params=("yours", Address("you", "yours"))))

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)
    me.receive(DummyQueryAddressResponse(), ..., ..., ...)

    assert cache.get_address("yours") == Address("you", "yours")


def test_should_use_cached_address_if_exists():
    cache = AddressCache()
    cache.update_cache(Address("you", "yours"))
    your_queue = MockQueue()
    me = create_messenger_for_test("me", address_cache=cache)
    you = create_messenger_for_test("you", inbox_queue=your_queue)
    me.make_connection_to(you)

    me.receive(MessageForwardRequest(DummyMessage(123), "mine", "yours"), ..., ..., ...)

    assert your_queue.get() == Packet(DummyMessage(123), sender=Address("me", "mine"), receiver=Address("you", "yours"))
