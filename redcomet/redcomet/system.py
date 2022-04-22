from redcomet.actor.abstract import ActorAbstract
from redcomet.actor.ref import ActorRef


class ActorSystem:
    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return ActorRef.of(actor)
