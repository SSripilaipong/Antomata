from redcomet.actor.abstract import ActorAbstract
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.node import NodeAbstract
from redcomet.node.register import RegisterActorRequest


class NodeManager(ActorAbstract):
    def __init__(self, actor_id: str, node: NodeAbstract, discovery: Address = None):
        self._actor_id = actor_id
        self._node = node
        self._discovery = discovery

    def bind_discovery(self, address: Address):
        self._discovery = address

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RegisterActorRequest):
            self._register(message)
        else:
            raise NotImplementedError()

    def _register(self, request: RegisterActorRequest):
        self._node.register_executable_actor(request.actor, request.actor_id)

        packet = Packet(RegisterAddressRequest(request.actor_id, self._node.node_id),
                        sender=Address.on_local(self._actor_id),
                        receiver=self._discovery)
        self._node.messenger.send_packet(packet)
