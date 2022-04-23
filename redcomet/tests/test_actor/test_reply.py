from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.context import Context
from redcomet.base.message.abstract import MessageAbstract
from redcomet.actor.ref import ActorRef
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
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
    def __init__(self, data: str, provider: ActorRef, recv_queue: QueueAbstract):
        self._data = data
        self._provider = provider
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract, sender: ActorRef, me: ActorRef):
        if isinstance(message, StartCommand):
            self._provider.tell(RequestMessage(self._data))
        elif isinstance(message, ResponseMessage):
            self._recv_queue.put(message.value)
        else:
            raise NotImplementedError()


class Provider(ActorAbstract):
    def __init__(self, data: str):
        self._data = data

    def receive(self, message: MessageAbstract, sender: ActorRef, me: ActorRef):
        if isinstance(message, RequestMessage):
            Context().sender.tell(ResponseMessage(message.value + self._data))
        else:
            raise NotImplementedError()


def test_should_response_back_to_sender():
    response_queue = DefaultQueue()
    with ActorSystem() as system:
        provider = system.spawn(Provider("Paste"))
        caller = system.spawn(Caller("Copy", provider, response_queue))
        caller.tell(StartCommand())

        assert response_queue.get(timeout=1) == "CopyPaste"
