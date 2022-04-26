from redcomet.base.actor import ActorAbstract
from redcomet.base.actor.message import MessageAbstract


class RegisterActorRequest(MessageAbstract):
    def __init__(self, actor_id: str, actor: ActorAbstract):
        self._actor_id = actor_id
        self._actor = actor

    @property
    def actor_id(self) -> str:
        return self._actor_id

    @property
    def actor(self) -> ActorAbstract:
        return self._actor
