import multiprocessing

from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.inbox import InboxAbstract
from redcomet.messenger.inbox.message import StopReceiveLoop
from redcomet.messenger.inbox.queue import QueueAbstract, QueueManagerAbstract


class ProcessSafeInbox(InboxAbstract):
    def __init__(self, manager: QueueManagerAbstract, queue: QueueAbstract, handler: PacketHandlerAbstract = None):
        self._manager = manager
        self._queue = queue
        self._handler = handler

    def set_handler(self, handler: PacketHandlerAbstract):
        self._handler = handler

    def receive(self, packet: Packet):
        self._queue.put(packet)

    def receive_loop(self):
        while True:
            packet = self._queue.get(block=True)
            print(multiprocessing.current_process().name, "RECV", packet)
            if isinstance(packet.content, StopReceiveLoop):
                break
            self._handler.handle(packet)

    def stop_receive_loop(self):
        self._queue.put(Packet(StopReceiveLoop(), sender=..., receiver=...))

    def close(self):
        self._manager.shutdown()
