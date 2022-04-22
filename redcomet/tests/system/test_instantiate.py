from multiprocessing import Queue

from redcomet.actor.abstract import ActorAbstract
from redcomet.message.abstract import MessageAbstract
from redcomet.system import ActorSystem


def test_should_tell_message():
    class MyActor(ActorAbstract):
        def __init__(self, recv_queue: Queue):
            self._recv_queue = recv_queue

        def receive(self, message: MessageAbstract):
            self._recv_queue.put(message)

    class MyMessage(MessageAbstract):
        def __init__(self, value: str):
            self.value = value

    queue = Queue()
    system = ActorSystem()
    ref = system.spawn(MyActor(queue))
    ref.tell(MyMessage("Hello"))

    recv_message = queue.get(timeout=2)
    assert recv_message.value == "Hello"
