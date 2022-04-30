from redcomet.actor.executor import ActorExecutor
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutor):
        self._actor_executor = actor_executor

    def handle(self, packet: Packet):
        content = packet.content
        if isinstance(content, MessageAbstract):
            local_receiver_id = packet.receiver.target
            sender_id = packet.sender.target
            self._actor_executor.execute(content, sender_id, local_receiver_id)
        else:
            raise NotImplementedError()
