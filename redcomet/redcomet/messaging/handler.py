from redcomet.actor.packet import ActorMessagePacket
from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import PacketAbstract


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract):
        self._actor_executor = actor_executor

    def handle(self, packet: PacketAbstract, sender_id: str, receiver_id: str):
        if isinstance(packet, ActorMessagePacket):
            local_receiver_id = receiver_id.split(".")[1]
            self._actor_executor.execute(packet.message, sender_id, local_receiver_id)
        else:
            raise NotImplementedError()
