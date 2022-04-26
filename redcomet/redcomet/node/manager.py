from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messaging.packet import Packet
from redcomet.node.register import RegisterActorRequest


class NodeManager(ActorAbstract):
    def __init__(self, actor_id: str, node_id: str, outbox: Outbox, executor: ActorExecutorAbstract,
                 discovery: Address):
        self._actor_id = actor_id
        self._node_id = node_id
        self._outbox = outbox
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

        packet = Packet(RegisterAddressRequest(request.actor_id, self._node_id),
                        sender=Address.on_local(self._actor_id),
                        receiver=self._discovery)
        self._outbox.send(packet)
