from redcomet.actor.ref import ActorRef
from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.cluster.abstract import ClusterAbstract


class Cluster(ClusterAbstract):
    def spawn(self, actor: ActorAbstract) -> ActorRef:
        return ActorRef.of(actor)
