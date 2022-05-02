from contextlib import suppress
from typing import Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.cluster.message.list_active_node.request import ListActiveNodeRequest
from redcomet.cluster.message.list_active_node.response import ListActiveNodeResponse
from redcomet.cluster.ref import ClusterRef


class MockDirectMessageBoxRef(DirectMessageBoxRefAbstract):
    def __init__(self, ref_id: str = None):
        self._ref_id = ref_id

    def put(self, item: MessageAbstract):
        pass

    def get(self, timeout: float) -> Any:
        return ListActiveNodeResponse([])

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __enter__(self) -> 'DirectMessageBoxRefAbstract':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockMessenger(MessengerAbstract):
    def create_direct_message_box(self) -> DirectMessageBoxRefAbstract:
        return MockDirectMessageBoxRef(self._generated_ref_id)

    def __init__(self, generated_ref_id: str = None):
        self._generated_ref_id = generated_ref_id
        self.sent_packet = None

    def send(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        pass

    def send_packet(self, packet: Packet):
        self.sent_packet = packet

    def assign_node_id(self, node_id: str):
        pass

    def bind_discovery(self, ref: ActorDiscoveryRefAbstract):
        pass

    def make_connection_to(self, other: 'MessengerAbstract'):
        pass

    @property
    def node_id(self) -> str:
        return ""


def test_should_send_list_active_node_message_cluster_manager():
    messenger = MockMessenger()
    cluster = ClusterRef(messenger, "me", "main", "cluster")

    with suppress(TimeoutError):
        cluster.get_active_nodes(timeout=0.001)

    assert isinstance(messenger.sent_packet.content, ListActiveNodeRequest)
