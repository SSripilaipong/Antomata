from redcomet.actor.ref import ActorRef
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system import ActorSystem


class MyStringMessage(MessageAbstract):
    def __init__(self, value: str):
        self.value = value


class IntroduceMessage(MessageAbstract):
    def __init__(self, ref: ActorRef):
        self.ref = ref


class First(ActorAbstract):

    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue
        self._second = None

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, IntroduceMessage):
            self._second = message.ref
        elif isinstance(message, MyStringMessage):
            if message.value == "hi to second":
                self._second.tell(MyStringMessage("HI FROM FIRST"))
            else:
                self._recv_queue.put(message.value)
        else:
            raise NotImplementedError()


class Second(ActorAbstract):
    def __init__(self, first: ActorRef, recv_queue: QueueAbstract):
        self._first = first
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, MyStringMessage):
            if message.value == "hi to first":
                self._first.tell(MyStringMessage("HI FROM SECOND"))
            else:
                self._recv_queue.put(message.value)
        else:
            raise NotImplementedError()


def test_should_communicate_between_actors():
    first_queue = DefaultQueue()
    second_queue = DefaultQueue()
    with ActorSystem.create() as system:
        first = system.spawn(First(first_queue))
        second = system.spawn(Second(first, second_queue))

        first.tell(IntroduceMessage(second))

        first.tell(MyStringMessage("hi to second"))
        message_second = second_queue.get(timeout=2)
        assert message_second == "HI FROM FIRST"

        second.tell(MyStringMessage("hi to first"))
        message_first = first_queue.get(timeout=2)
        assert message_first == "HI FROM SECOND"
