import os
import uuid
from typing import List

from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.cluster.message.list_active_node.request import ListActiveNodeRequest
from redcomet.cluster.message.list_active_node.response import ListActiveNodeResponse
from redcomet.cluster.message.spawn_actor.request import SpawnActorRequest
from redcomet.node.ref import NodeRef


class ClusterRef(ClusterRefAbstract):
    def __init__(self, messenger: MessengerAbstract, issuer_id: str, ref_node_id: str, ref_id: str):
        self._messenger = messenger
        self._issuer_id = issuer_id
        self._address = Address(ref_node_id, ref_id)

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        ref_id = _generate_actor_id()
        packet = Packet(SpawnActorRequest(actor, ref_id),
                        sender=Address.on_local(self._issuer_id),
                        receiver=self._address)
        self._messenger.send_packet(packet)
        return ActorRef(self._messenger, self._issuer_id, Address.anywhere(ref_id))

    def get_active_nodes(self, timeout: float) -> List[NodeRef]:
        with self._messenger.create_direct_message_box() as box:
            packet = Packet(ListActiveNodeRequest(box.ref_id),
                            sender=Address.on_local("messenger"),
                            receiver=self._address)
            self._messenger.send_packet(packet)
            response: ListActiveNodeResponse = box.get(timeout=timeout)
        return [NodeRef(self._messenger, self._issuer_id, node_id) for node_id in response.node_ids]


def _generate_actor_id() -> str:
    return uuid.UUID(bytes=os.urandom(16), version=4).hex
