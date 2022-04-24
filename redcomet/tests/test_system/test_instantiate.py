from redcomet.base.actor import ActorRefAbstract
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.base.messaging.message import MessageAbstract
from redcomet.queue.abstract import QueueAbstract
from redcomet.queue.default import DefaultQueue
from redcomet.system import ActorSystem


class MyStringMessage(MessageAbstract):
    def __init__(self, value: str):
        self.value = value


class MyActor(ActorAbstract):
    def __init__(self, recv_queue: QueueAbstract):
        self._recv_queue = recv_queue

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterAbstract):
        self._recv_queue.put(message)


def test_should_tell_message():
    queue = DefaultQueue()
    with ActorSystem.create() as system:
        ref = system.spawn(MyActor(queue))
        ref.tell(MyStringMessage("Hello"))

        recv_message = queue.get(timeout=2)

    assert recv_message.value == "Hello"
