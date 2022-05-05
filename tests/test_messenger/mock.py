from queue import Queue
from typing import Any, Optional, Callable, Tuple

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.discovery.ref import ActorDiscoveryRefAbstract
from redcomet.base.messaging.address import Address

from redcomet.base.messaging.content import PacketContentAbstract
from redcomet.base.messaging.handler import PacketHandlerAbstract
from redcomet.base.messaging.packet import Packet

from redcomet.messenger.inbox.queue import QueueAbstract, QueueManagerAbstract
from redcomet.messenger.handler.executor.actor import ActorExecutorAbstract


class MockQueue(QueueAbstract):
    def __init__(self):
        self._queue = Queue()

    def put(self, obj: Any, block: bool = True, timeout: float = None):
        self._queue.put(obj)

    def get(self, block: bool = True, timeout: float = None) -> Any:
        return self._queue.get()

    def empty(self) -> bool:
        return self._queue.empty()


class MockQueueManager(QueueManagerAbstract):
    def start(self) -> QueueAbstract:
        pass

    def shutdown(self):
        pass


class MockActorExecutor(ActorExecutorAbstract):
    def __init__(self):
        self.received_message: Optional[Tuple[PacketContentAbstract, Address, str]] = None

    def register(self, local_id: str, actor: ActorAbstract):
        pass

    def execute(self, message: PacketContentAbstract, sender: Address, local_actor_id: str):
        self.received_message = (message, sender, local_actor_id)


class DummyPacketContent(PacketContentAbstract):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self) -> str:
        return f"DummyPacketContent({self.value!r})"

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, DummyPacketContent)
        return self.value == other.value


class MockActorDiscoveryRef(ActorDiscoveryRefAbstract):
    def __init__(self, query_response_params=None):
        self._query_response_params = query_response_params
        self.queried_address = None

    def register_address(self, target: str, node_id: str):
        pass

    def query_address(self, target: str, requester_node_id: str, requester_target: str):
        self.queried_address = target, requester_node_id, requester_target

    def call_on_query_address_response(self, message: MessageAbstract, func: Callable[[str, Address], Any]) -> bool:
        if not isinstance(message, DummyQueryAddressResponse):
            return False
        if self._query_response_params:
            func(*self._query_response_params)
            return True
        return False


class DummyQueryAddressResponse(MessageAbstract):
    pass


class DummyMessage(MessageAbstract):
    def __init__(self, value, ref_id: str = None):
        self.value = value
        self._ref_id = ref_id

    @property
    def ref_id(self) -> str:
        return self._ref_id

    def __repr__(self):
        return f"DummyMessage({self.value!r}, ref_id={self.ref_id!r})"

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, DummyMessage)
        return self.value == other.value and self.ref_id == other.ref_id
