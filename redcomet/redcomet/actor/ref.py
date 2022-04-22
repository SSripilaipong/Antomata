from redcomet.actor.abstract import ActorAbstract
from redcomet.message.abstract import MessageAbstract


class ActorRef:
    def __init__(self, actor: ActorAbstract):
        self._actor = actor

    def tell(self, message: MessageAbstract):
        self._actor.handle_message(message)

    @classmethod
    def of(cls, actor: ActorAbstract) -> 'ActorRef':
        return ActorRef(actor)
