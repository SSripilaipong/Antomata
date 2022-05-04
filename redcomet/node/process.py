from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.node.ref import NodeRef


class ProcessNode(NodeAbstract):
    def bind_discovery(self, address: Address):
        pass

    def issue_actor_ref(self, local_issuer_id: str, address: Address) -> ActorRefAbstract:
        pass

    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        pass

    def issue_node_ref(self, local_issuer_id: str, node_id: str) -> NodeRef:
        pass

    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        pass

    def assign_node_id(self, node_id: str):
        pass

    @property
    def node_id(self) -> str:
        pass

    @property
    def messenger(self) -> MessengerAbstract:
        pass

    def make_connection_to(self, node: 'NodeAbstract'):
        pass
