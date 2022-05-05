from multiprocessing import Process
from typing import Optional

from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.cluster.ref import ClusterRef
from redcomet.discovery.ref import ActorDiscoveryRef
from redcomet.messenger.handler.executor.actor import ActorExecutorAbstract
from redcomet.node.manager.abstract import NodeManagerAbstract
from redcomet.node.ref import NodeRef


class ProcessNode(NodeAbstract):
    def __init__(self, messenger: MessengerAbstract, executor: ActorExecutorAbstract):
        self._messenger = messenger
        self._executor = executor

        self._manager: Optional[NodeManagerAbstract] = None
        self._actor_id: Optional[str] = None
        self._node_id: Optional[str] = None

    def bind_discovery(self, address: Address):
        ref = ActorDiscoveryRef(self._messenger, address, self._actor_id)
        self._messenger.bind_discovery(ref)
        self._manager.bind_discovery(ref)

    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        return ClusterRef(self._messenger, local_issuer_id, "main", "cluster")

    def issue_actor_ref(self, local_issuer_id: str, address: Address) -> ActorRefAbstract:
        return ActorRef(self._messenger, local_issuer_id, address)

    def issue_node_ref(self, local_issuer_id: str, node_id: str) -> NodeRef:
        return NodeRef(self._messenger, local_issuer_id, node_id)

    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        self._executor.register(actor_id, actor)

    def assign_node_id(self, node_id: str):
        self._node_id = node_id
        self._actor_id = node_id
        self._messenger.assign_node_id(node_id)

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def messenger(self) -> MessengerAbstract:
        return self._messenger

    def make_connection_to(self, node: 'NodeAbstract'):
        self._messenger.make_connection_to(node.messenger)

    def assign_manager(self, manager: NodeManagerAbstract):
        self._manager = manager

    def start(self):
        Process(target=self._messenger.start_receive_loop).start()

    def stop(self):
        self._messenger.stop_receive_loop()

    def close(self):
        self._messenger.close()
