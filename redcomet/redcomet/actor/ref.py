from redcomet.message.abstract import MessageAbstract


class ActorRef:
    def tell(self, message: MessageAbstract):
        raise NotImplementedError()
