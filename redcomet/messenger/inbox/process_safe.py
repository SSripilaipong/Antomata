from multiprocessing.queues import Queue

from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet
from redcomet.messenger.inbox import InboxAbstract
from redcomet.messenger.inbox.message import StopReceiveLoop


class ProcessSafeInbox(InboxAbstract):
    def __init__(self, queue: Queue, handler: PacketHandlerAbstract = None):
        self._queue = queue
        self._handler = handler

    def set_handler(self, handler: PacketHandlerAbstract):
        self._handler = handler

    def receive(self, packet: Packet):
        self._queue.put(packet)

    def receive_loop(self):
        while True:
            packet = self._queue.get()
            if isinstance(packet.content, StopReceiveLoop):
                break
            self._handler.handle(packet)

    def stop_receive_loop(self):
        self._queue.put(Packet(StopReceiveLoop(), sender=..., receiver=...))

    def close(self):
        self._queue.close()
        self._queue.join_thread()
