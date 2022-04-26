from typing import Dict

from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.query import QueryAddressRequest, QueryAddressResponse
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messaging.packet import Packet


class ActorDiscovery(ActorAbstract):
    def __init__(self, actor_id: str, node_id: str, outbox: Outbox = None):
        self._actor_id = actor_id
        self._node_id = node_id
        self._outbox = outbox

        self._mapper: Dict[str, str] = {}

    @classmethod
    def create(cls, actor_id: str, node_id: str) -> 'ActorDiscovery':
        discovery = cls(actor_id, node_id)
        discovery._register(node_id, node_id)
        discovery._register(actor_id, node_id)
        return discovery

    def set_outbox(self, outbox: Outbox):
        self._outbox = outbox

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RegisterAddressRequest):
            self._process_register_request(message)
        elif isinstance(message, QueryAddressRequest):
            self._process_query_address_request(message)
        else:
            raise NotImplementedError()

    def _process_register_request(self, message: RegisterAddressRequest):
        self._register(message.target, message.node_id)

    def _process_query_address_request(self, message: QueryAddressRequest):
        node_id = self._query_node_id(message.target)
        address = Address(node_id, message.target)
        packet = Packet(QueryAddressResponse(message.target, address),
                        sender=Address(self._node_id, self._actor_id),
                        receiver=Address(message.requester_node_id, message.requester_target))
        self._outbox.send(packet)

    def _register(self, target: str, node_id: str):
        if target in self._mapper:
            raise NotImplementedError()
        self._mapper[target] = node_id

    def _query_node_id(self, target: str) -> str:
        node_id = self._mapper.get(target)
        if node_id is None:
            raise NotImplementedError()
        return node_id
