from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.packet import Packet
from redcomet.base.messenger.abstract import MessengerAbstract
from redcomet.node.register import RegisterActorRequest


class NodeRef:
    def __init__(self, messenger: MessengerAbstract, issuer_id: str, node_id: str):
        self._messenger = messenger
        self._issuer_id = issuer_id
        self._node_id = node_id

    def is_active(self, timeout: float) -> bool:
        return False

    @property
    def node_id(self) -> str:
        return self._node_id

    def register_address(self, node_id: str, actor_id: str, actor: ActorAbstract):
        message = RegisterActorRequest(actor_id, actor)
        packet = Packet(message, Address.on_local(self._issuer_id), Address(node_id, "manager"))
        self._messenger.send_packet(packet)
