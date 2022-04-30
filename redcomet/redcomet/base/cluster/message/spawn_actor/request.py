from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor.message import MessageAbstract


class SpawnActorRequest(MessageAbstract):
    def __init__(self, actor: ActorAbstract, actor_id: str):
        self._actor = actor
        self._actor_id = actor_id

    @property
    def actor(self) -> ActorAbstract:
        return self._actor

    @property
    def actor_id(self) -> str:
        return self._actor_id

    def __repr__(self) -> str:
        return f"SpawnActorRequest(actor={self.actor}, actor_id={self.actor_id})"
