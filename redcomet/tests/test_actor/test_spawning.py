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


class MyActor(ActorAbstract):
    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue
        self._another = None

    def receive(self, message: MyStringMessage, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if message.value == "start":
            self._another = cluster.spawn(AnotherActor(self._recv_queue))
        elif message.value == "hi to another":
            self._another.tell(MyStringMessage("HI"))
        else:
            raise NotImplementedError()


class AnotherActor(ActorAbstract):
    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        self._recv_queue.put(message)


def test_should_tell_message_to_another_actor():
    queue = DefaultQueue()
    with ActorSystem.create() as system:
        my_actor = system.spawn(MyActor(queue))

        my_actor.tell(MyStringMessage("start"))
        my_actor.tell(MyStringMessage("hi to another"))
        recv_message = queue.get(timeout=2)

    assert recv_message.value == "HI"
