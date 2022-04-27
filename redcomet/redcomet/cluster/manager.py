from typing import List

from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.cluster.request import SpawnActorRequest
from redcomet.base.discovery import ActorDiscovery
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.node import NodeAbstract
from redcomet.node.register import RegisterActorRequest


class ClusterManager(ActorAbstract):
    def __init__(self, node: NodeAbstract, actor_id: str, discovery: ActorDiscovery):
        self._node = node
        self._actor_id = actor_id
        self._discovery = discovery

        self._nodes: List[NodeAbstract] = []
        self._node_index = 0

    @classmethod
    def create(cls, node: NodeAbstract, actor_id: str) -> 'ClusterManager':
        discovery = ActorDiscovery.create("discovery", "main")
        cluster = cls(node, actor_id, discovery)
        discovery.register_address("cluster", "main")

        node.bind_discovery(discovery.address)
        node.make_connection_to(node)
        discovery.set_node(node)
        node.register_executable_actor(discovery, discovery.address.target)

        return cluster

    def add_node(self, node: NodeAbstract, node_id: str):
        if node in self._nodes or node is self._node:
            raise NotImplementedError()

        node.bind_discovery(self._discovery.address)
        node.make_connection_with(self._node)
        for existing_node in self._nodes:
            existing_node.make_connection_with(node)
        node.make_connection_to(node)

        self._nodes.append(node)

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, SpawnActorRequest):
            self._process_spawn_request(message)
        else:
            raise NotImplementedError()

    def _process_spawn_request(self, message: SpawnActorRequest):
        node_id = self._get_node_id()
        self._request_register_address(node_id, message.actor_id, message.actor)

    def _get_node_id(self) -> str:
        if self._node_index >= len(self._nodes):
            self._node_index = 0
        node_id = self._nodes[self._node_index].node_id
        self._node_index += 1
        return node_id

    def _request_register_address(self, node_id: str, actor_id: str, actor: ActorAbstract):
        message = RegisterActorRequest(actor_id, actor)
        packet = Packet(message, Address.on_local(self._actor_id), Address(node_id, "manager"))
        self._node.messenger.send_packet(packet)
