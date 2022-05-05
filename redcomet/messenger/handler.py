from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.direct_message.manager import DirectMessageManager
from redcomet.node.executor import ActorExecutorAbstract


class PacketHandler(PacketHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract, direct_message_manager: DirectMessageManager = None):
        self._actor_executor = actor_executor
        self._direct_message_manager = direct_message_manager

    def handle(self, packet: Packet):
        content = packet.content
        if isinstance(content, MessageAbstract) and content.ref_id is not None:
            self._direct_message_manager.get_message_box(content.ref_id).put(content)
        else:
            assert isinstance(content, PacketContentAbstract)
            local_receiver_id = packet.receiver.target
            self._actor_executor.execute(content, packet.sender, local_receiver_id)
