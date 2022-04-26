from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address


class QueryAddressRequest(MessageAbstract):
    def __init__(self, target: str, requester_node_id: str, requester_target: str):
        self._target = target
        self._requester_node_id = requester_node_id
        self._requester_target = requester_target

    @property
    def target(self) -> str:
        return self._target

    @property
    def requester_node_id(self) -> str:
        return self._requester_node_id

    @property
    def requester_target(self) -> str:
        return self._requester_target


class QueryAddressResponse(MessageAbstract):
    def __init__(self, target: str, address: Address):
        self._target = target
        self._address = address

    @property
    def target(self) -> str:
        return self._target

    @property
    def address(self) -> Address:
        return self._address
