from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.node import NodeAbstract
from redcomet.node.register import RegisterActorRequest


class NodeManager(ActorAbstract):
    def __init__(self, actor_id: str, node: NodeAbstract, executor: ActorExecutorAbstract,
                 discovery: Address):
        self._actor_id = actor_id
        self._node = node
        self._executor = executor
        self._discovery = discovery

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RegisterActorRequest):
            self._register(message)
        else:
            raise NotImplementedError()

    def _register(self, request: RegisterActorRequest):
        self._executor.register(request.actor_id, request.actor)

        packet = Packet(RegisterAddressRequest(request.actor_id, self._node.node_id),
                        sender=Address.on_local(self._actor_id),
                        receiver=self._discovery)
        self._node.messenger.send_packet(packet)
