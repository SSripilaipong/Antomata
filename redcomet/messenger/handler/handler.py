from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.handler.executor.actor import ActorExecutorAbstract
from redcomet.messenger.handler.executor.messenger_command import MessengerCommandExecutor


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract, messenger_command_executor: MessengerCommandExecutor):
        self._actor_executor = actor_executor
        self._messenger_command_executor = messenger_command_executor

    def handle(self, packet: Packet):
        if self._messenger_command_executor.filter_packet(packet):
            pass
        else:
            content = packet.content
            assert isinstance(content, PacketContentAbstract)
            local_receiver_id = packet.receiver.target
            self._actor_executor.execute(content, packet.sender, local_receiver_id)
