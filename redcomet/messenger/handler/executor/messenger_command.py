from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.direct_message.manager import DirectMessageManager
from redcomet.messenger.inbox.exception import StopReceiveLoopException
from redcomet.messenger.inbox.message import StopReceiveLoop


class MessengerCommandExecutor:
    def __init__(self, direct_message_manager: DirectMessageManager):
        self._direct_message_manager = direct_message_manager

    def filter_packet(self, packet: Packet) -> bool:
        content = packet.content
        if isinstance(content, MessageAbstract) and content.ref_id is not None:
            self._direct_message_manager.get_message_box(content.ref_id).put(content)
            return True
        elif isinstance(packet.content, StopReceiveLoop):
            raise StopReceiveLoopException()
        return False
