from redcomet.base.actor.executor import ActorExecutorAbstract
from redcomet.base.messaging.handler import MessageHandlerAbstract
from redcomet.base.messaging.message import MessageAbstract


class MessageHandler(MessageHandlerAbstract):
    def __init__(self, actor_executor: ActorExecutorAbstract):
        self._actor_executor = actor_executor

    def handle(self, message: MessageAbstract, sender_id: str, receiver_id: str):
        local_receiver_id = receiver_id.split(".")[1]
        self._actor_executor.execute(message, sender_id, local_receiver_id)
