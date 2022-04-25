from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.abstract import ClusterAbstract
from redcomet.system import ActorSystem


class Ping(MessageAbstract):
    pass


class Pong(MessageAbstract):
    pass


class MyActor(ActorAbstract):
    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterAbstract):
        if isinstance(message, Ping):
            sender.tell(Pong())
        else:
            raise NotImplementedError()


def test_should_reply_to_gateway():
    with ActorSystem.create() as system:
        actor = system.spawn(MyActor())
        actor.tell(Ping())
        reply = system.fetch_message(timeout=1)
        assert isinstance(reply, Pong)
