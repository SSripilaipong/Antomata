from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.cluster.request import SpawnActorRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.messenger import MessengerAbstract


class ClusterRef(ClusterRefAbstract):
    def __init__(self, messenger: MessengerAbstract = None, issuer_id: str = None):
        self._messenger = messenger
        self._issuer_id = issuer_id

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        ref_id = _generate_actor_id(actor)
        packet = Packet(SpawnActorRequest(actor, ref_id),
                        sender=Address.on_local(self._issuer_id),
                        receiver=Address("main", "cluster"))
        self._messenger.send_packet(packet)
        return ActorRef(self._messenger, self._issuer_id, ref_id)


def _generate_actor_id(actor: ActorAbstract) -> str:
    return str(id(actor))
