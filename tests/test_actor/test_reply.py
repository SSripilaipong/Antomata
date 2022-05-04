from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.manager import ProcessSafeQueue
from redcomet.system import ActorSystem


class RequestMessage(MessageAbstract):
    def __init__(self, value: str):
        self.value = value


class ResponseMessage(MessageAbstract):
    def __init__(self, value: str):
        self.value = value


class StartCommand(MessageAbstract):
    pass


class Caller(ActorAbstract):
    def __init__(self, data: str, provider: Address, recv_queue: QueueAbstract):
        self._data = data
        self._provider = ActorRef(..., ..., provider)
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRef,
                cluster: ClusterRefAbstract):
        self._provider = self._provider.bind(me)  # TODO: find better way to set local_id
        if isinstance(message, StartCommand):
            self._provider.tell(RequestMessage(self._data))
        elif isinstance(message, ResponseMessage):
            self._recv_queue.put(message.value)
        else:
            raise NotImplementedError()


class Provider(ActorAbstract):
    def __init__(self, data: str):
        self._data = data

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RequestMessage):
            sender.tell(ResponseMessage(message.value + self._data))
        else:
            raise NotImplementedError()


def test_should_response_back_to_sender():
    with ProcessSafeQueue() as response_queue:
        with ActorSystem.create(parallel=True) as system:
            provider = system.spawn(Provider("Paste"))
            caller = system.spawn(Caller("Copy", provider.address, response_queue))
            caller.tell(StartCommand())

            assert response_queue.get(timeout=0.1) == "CopyPaste"
