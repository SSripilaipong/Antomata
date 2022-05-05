from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.node.executor import ActorExecutorAbstract


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract):
        self._actor_executor = actor_executor

    def handle(self, packet: Packet):
        content = packet.content
        assert isinstance(content, PacketContentAbstract)
        local_receiver_id = packet.receiver.target
        self._actor_executor.execute(content, packet.sender, local_receiver_id)
