from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address


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
