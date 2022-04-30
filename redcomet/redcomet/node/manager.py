from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.node.abstract import NodeAbstract
from redcomet.node.register import RegisterActorRequest


class NodeManager(ActorAbstract):
    def __init__(self, actor_id: str, node: NodeAbstract, discovery: ActorDiscoveryRefAbstract = None):
        self._actor_id = actor_id
        self._node = node
        self._discovery = discovery

    def bind_discovery(self, discovery: ActorDiscoveryRefAbstract):
        self._discovery = discovery

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RegisterActorRequest):
            self._register(message)
        else:
            raise NotImplementedError()

    def _register(self, request: RegisterActorRequest):
        self._node.register_executable_actor(request.actor, request.actor_id)
        self._discovery.register_address(request.actor_id, self._node.node_id)
