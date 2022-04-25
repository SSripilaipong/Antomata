from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract):
        self._actor_executor = actor_executor

    def handle(self, packet: Packet, sender_id: str, receiver_id: str):
        content = packet.content
        if isinstance(content, MessageAbstract):
            local_receiver_id = receiver_id.split(".")[1]
            self._actor_executor.execute(content, sender_id, local_receiver_id)
        else:
            raise NotImplementedError()
