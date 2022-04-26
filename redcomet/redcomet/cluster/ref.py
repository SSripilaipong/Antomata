from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.messenger import MessengerAbstract
from redcomet.base.node import NodeAbstract
from redcomet.node.register import RegisterActorRequest


class ClusterRef(ClusterRefAbstract):
    def __init__(self, messenger: MessengerAbstract = None):
        self._messenger = messenger
        self._default_local_sender_id = None
        self._default_sender_node = None

    def set_messenger(self, messenger: MessengerAbstract):
        self._messenger = messenger

    def set_default_sender_node(self, node: NodeAbstract):
        self._default_sender_node = node

    def set_default_local_sender_id(self, local_id: str):
        self._default_local_sender_id = local_id

    def spawn(self, actor: ActorAbstract, local_messenger: MessengerAbstract = None, local_sender_id: str = None) \
            -> ActorRefAbstract:
        ref_id = _generate_actor_id(actor)
        local_sender_id = local_sender_id or self._default_local_sender_id
        packet = Packet(RegisterActorRequest(ref_id, actor),
                        sender=Address.on_local(local_sender_id),
                        receiver=Address("node0", "manager"))
        self._messenger.send_packet(packet)
        return ActorRef(local_messenger or self._messenger, local_sender_id, ref_id)


def _generate_actor_id(actor: ActorAbstract) -> str:
    return str(id(actor))
