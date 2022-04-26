from typing import Dict

from redcomet.base.actor import ActorAbstract, ActorRefAbstract
from redcomet.base.actor.message import MessageAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.discovery.query import QueryAddressRequest, QueryAddressResponse
from redcomet.base.discovery.register import RegisterAddressRequest
from redcomet.base.messaging.address import Address


class ActorDiscovery(ActorAbstract):
    def __init__(self):
        self._mapper: Dict[str, str] = {}

    @classmethod
    def create(cls, node_id: str) -> 'ActorDiscovery':
        discovery = cls()
        discovery._register(node_id, node_id)
        discovery._register("discovery", node_id)
        return discovery

    def receive(self, message: MessageAbstract, sender: ActorRefAbstract, me: ActorRefAbstract,
                cluster: ClusterRefAbstract):
        if isinstance(message, RegisterAddressRequest):
            self._process_register_request(message)
        elif isinstance(message, QueryAddressRequest):
            self._query_address(message, sender)
        else:
            raise NotImplementedError()

    def _process_register_request(self, message: RegisterAddressRequest):
        self._register(message.target, message.node_id)

    def _query_address(self, message: QueryAddressRequest, sender: ActorRefAbstract):
        node_id = self.query_node_id(message.target)
        address = Address(node_id, message.target)
        sender.tell(QueryAddressResponse(message.target, address))

    def _register(self, target: str, node_id: str):
        if target in self._mapper:
            raise NotImplementedError()
        self._mapper[target] = node_id

    def query_node_id(self, target: str) -> str:
        node_id = self._mapper.get(target)
        if node_id is None:
            raise NotImplementedError()
        return node_id
