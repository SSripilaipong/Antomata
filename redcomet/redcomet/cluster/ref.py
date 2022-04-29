from multiprocessing import Queue
from typing import List

from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.cluster.message.list_active_node.request import ListActiveNodeRequest
from redcomet.base.cluster.message.spawn_actor.request import SpawnActorRequest
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.messenger import MessengerAbstract
from redcomet.node.ref import NodeRef


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

    def get_active_nodes(self, timeout: float) -> List[NodeRef]:
        reply_queue = Queue()
        packet = Packet(ListActiveNodeRequest(reply_queue),
                        sender=Address.on_local(self._issuer_id),
                        receiver=Address("main", "cluster"))
        self._messenger.send_packet(packet)
        node_ids = reply_queue.get(timeout=timeout)
        return [NodeRef(node_id) for node_id in node_ids]


def _generate_actor_id(actor: ActorAbstract) -> str:
    return str(id(actor))
