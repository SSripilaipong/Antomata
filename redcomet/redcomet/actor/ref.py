from redcomet.base.actor.abstract import ActorAbstract
from redcomet.actor.wrapper import ActorWrapper
from redcomet.base.context import Context
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract


class ActorRef(ActorRefAbstract):
    def __init__(self, actor: ActorWrapper):
        self._actor = actor

    def tell(self, message: MessageAbstract):
        self._actor.handle_message(Context().me, message)

    @classmethod
    def of(cls, actor: ActorAbstract) -> 'ActorRef':
        wrapper = ActorWrapper(actor)
        ref = ActorRef(wrapper)
        wrapper.set_my_ref(ref)
        return ref
