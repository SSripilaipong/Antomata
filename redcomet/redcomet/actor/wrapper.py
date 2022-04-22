from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.context import Context
from redcomet.base.actor.ref import ActorRefAbstract
from redcomet.base.message.abstract import MessageAbstract


class ActorWrapper:
    def __init__(self, actor: ActorAbstract, me: ActorRefAbstract = None):
        self._actor = actor
        self._me = me

    def set_my_ref(self, me: ActorRefAbstract):
        self._me = me

    def handle_message(self, sender: ActorRefAbstract, message: MessageAbstract):
        with Context().overwrite_ref(sender, self._me):
            self._actor.receive(message)
