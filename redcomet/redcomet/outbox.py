from redcomet.base.message.abstract import MessageAbstract
from redcomet.base.node import NodeAbstract
from redcomet.base.outbox import OutboxAbstract


class Outbox(OutboxAbstract):
    def __init__(self, node_id: str, local_node: NodeAbstract = None):
        self._node_id = node_id
        self._local_node = local_node

    def set_node(self, node: NodeAbstract):
        self._local_node = node

    def send(self, message: MessageAbstract, local_id: str, receiver_id: str):
        sender_id = f'{self._node_id}.{local_id}'
        self._find_node(receiver_id).receive(message, sender_id, receiver_id)

    def _find_node(self, _: str) -> NodeAbstract:
        return self._local_node
