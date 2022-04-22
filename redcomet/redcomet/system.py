from redcomet.actor.abstract import ActorAbstract
from redcomet.actor.ref import ActorRef


class ActorSystem:
    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return ActorRef.of(actor)

    def __enter__(self) -> 'ActorSystem':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
