from redcomet.base.actor.abstract import ActorAbstract
from redcomet.actor.ref import ActorRef
from redcomet.base.context import Context
from redcomet.cluster import Cluster


class ActorSystem:
    def __init__(self):
        Context().set_cluster(Cluster())

    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return ActorRef.of(actor)

    def __enter__(self) -> 'ActorSystem':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
