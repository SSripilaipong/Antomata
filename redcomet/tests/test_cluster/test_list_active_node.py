from typing import Any

from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.messenger.direct_message.ref import DirectMessageBoxRefAbstract
from redcomet.cluster.manager import ClusterManager
from redcomet.cluster.message.list_active_node.request import ListActiveNodeRequest
from redcomet.cluster.message.list_active_node.response import ListActiveNodeResponse
from redcomet.cluster.ref import ClusterRef


class MockDirectMessageBoxRef(DirectMessageBoxRefAbstract):
    def __init__(self, ref_id: str = None, active_node_response: MessageAbstract = None):
        self._ref_id = ref_id
        self._active_node_response = active_node_response or ListActiveNodeResponse([], "")

    def put(self, item: MessageAbstract):
        pass

    def get(self, timeout: float) -> Any:
        return self._active_node_response

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __enter__(self) -> 'DirectMessageBoxRefAbstract':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockMessenger(MessengerAbstract):
    def create_direct_message_box(self) -> DirectMessageBoxRefAbstract:
        return MockDirectMessageBoxRef(self._generated_ref_id, active_node_response=self._active_node_response)

    def __init__(self, generated_ref_id: str = None, active_node_response: MessageAbstract = None):
        self._generated_ref_id = generated_ref_id
        self._active_node_response = active_node_response
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


class MockActorRef(ActorRefAbstract):
    def __init__(self):
        self.told_message = None

    def tell(self, message: MessageAbstract):
        self.told_message = message

    def bind(self, ref: 'ActorRefAbstract') -> 'ActorRefAbstract':
        pass

    @property
    def ref_id(self) -> str:
        return ""


def test_should_send_list_active_node_message_cluster_manager():
    messenger = MockMessenger()
    cluster = ClusterRef(messenger, "me", "main", "cluster")

    cluster.get_active_nodes(timeout=0.001)

    assert isinstance(messenger.sent_packet.content, ListActiveNodeRequest)


def test_should_get_node_ids_in_list_active_response_from_direct_message_box():
    messenger = MockMessenger(active_node_response=ListActiveNodeResponse(["node1", "node999"], ""))
    cluster = ClusterRef(messenger, "me", "main", "cluster")

    assert [node.node_id for node in cluster.get_active_nodes(timeout=0.001)] == ["node1", "node999"]


def test_manager_should_send_back_list_active_response_with_ref_id():
    cluster = ClusterManager(..., "cluster", ...)
    sender = MockActorRef()
    cluster.receive(ListActiveNodeRequest("abc"), sender, ..., ...)
    response: ListActiveNodeResponse = sender.told_message
    assert response.ref_id == "abc"
