from typing import List, Dict

from redcomet.base.actor.abstract import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.node.abstract import NodeAbstract
from redcomet.base.node.ref import NodeRefAbstract
from redcomet.cluster.message.list_active_node.request import ListActiveNodeRequest
from redcomet.cluster.message.list_active_node.response import ListActiveNodeResponse
from redcomet.cluster.message.spawn_actor.request import SpawnActorRequest
from redcomet.discovery.actor import ActorDiscovery


class ClusterManager(ActorAbstract):
    def __init__(self, node: NodeAbstract, actor_id: str, discovery: Address,
                 node_refs: Dict[str, NodeRefAbstract] = None, nodes: List[NodeAbstract] = None):
        self._node = node
        self._actor_id = actor_id
        self._discovery = discovery

        self._nodes: List[NodeAbstract] = nodes or []

        self._node_refs = node_refs or {}
        self._node_ref_list: List[NodeRefAbstract] = [ref for ref in self._node_refs.values()]
        self._node_spawn_index = 0

    @classmethod
    def create(cls, node: NodeAbstract, node_id: str, actor_id: str) -> 'ClusterManager':
        discovery = ActorDiscovery.create("discovery", node_id)
        cluster = cls(node, actor_id, discovery.address)
        discovery.register_address(actor_id, node_id)

        node.assign_node_id(node_id)
        node.bind_discovery(discovery.address)
        discovery.set_node(node)

        node.register_executable_actor(cluster, actor_id)
        node.register_executable_actor(discovery, discovery.address.target)

        return cluster

    def add_node(self, node: NodeAbstract, node_id: str):
        if node in self._nodes or node is self._node:
            raise NotImplementedError()

        node.assign_node_id(node_id)
        self._make_node_connection(node)
        self._save_node_ref(node_id)

    def _save_node_ref(self, node_id):
        ref = self._node.issue_node_ref(self._actor_id, node_id)
        self._node_refs[node_id] = ref
        self._node_ref_list.append(ref)

    def _make_node_connection(self, node: NodeAbstract):
        node.bind_discovery(self._discovery)
        node.make_connection_with(self._node)
        for existing_node in self._nodes:
            existing_node.make_connection_with(node)
        self._nodes.append(node)

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, SpawnActorRequest):
            self._process_spawn_request(message)
        elif isinstance(message, ListActiveNodeRequest):
            self._process_list_active_node_request(message, sender)
        else:
            raise NotImplementedError()

    def _process_list_active_node_request(self, message: ListActiveNodeRequest, sender: ActorRefAbstract):
        node_ids = [node_id for node_id in self._node_refs.keys()]
        sender.tell(ListActiveNodeResponse(node_ids, ref_id=message.reply_ref_id))

    def _process_spawn_request(self, message: SpawnActorRequest):
        node_id = self._get_node_id()
        self._request_register_address(node_id, message.actor_id, message.actor)

    def _get_node_id(self) -> str:
        if self._node_spawn_index >= len(self._node_ref_list):
            self._node_spawn_index = 0
        node_id = self._node_ref_list[self._node_spawn_index].node_id
        self._node_spawn_index += 1
        return node_id

    def _request_register_address(self, node_id: str, actor_id: str, actor: ActorAbstract):
        ref = self._node_refs.get(node_id)
        if ref is None:
            raise NotImplementedError()
        ref.register_address(actor_id, actor)
