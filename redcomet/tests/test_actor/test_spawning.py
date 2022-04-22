from redcomet.actor.abstract import ActorAbstract
from redcomet.actor.ref import ActorRef
from redcomet.message.abstract import MessageAbstract
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system import ActorSystem


class MyStringMessage(MessageAbstract):
    def __init__(self, value: str):
        self.value = value


class Context:
    def spawn(self, actor: ActorAbstract) -> ActorRef:
        pass


class MyActor(ActorAbstract):
    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue
        self._another = None

    def receive(self, message: MyStringMessage):
        if message.value == "start":
            self._another = Context().spawn(AnotherActor(self._recv_queue))
        elif message.value == "hi to another":
            self._another.tell(MyStringMessage("HI"))
        else:
            raise NotImplementedError()


class AnotherActor(ActorAbstract):
    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract):
        self._recv_queue.put(message)


def test_should_tell_message_to_another_actor():
    queue = DefaultQueue()
    system = ActorSystem()
    my_actor = system.spawn(MyActor(queue))

    my_actor.tell(MyStringMessage("start"))
    my_actor.tell(MyStringMessage("hi to another"))
    recv_message = queue.get(timeout=2)

    assert recv_message.value == "HI"

    system.stop()
