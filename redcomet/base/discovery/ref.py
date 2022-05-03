from abc import ABC, abstractmethod
from typing import Callable, Any

from redcomet.base.actor.message import MessageAbstract
from redcomet.base.messaging.address import Address


class ActorDiscoveryRefAbstract(ABC):

    @abstractmethod
    def register_address(self, target: str, node_id: str):
        pass

    @abstractmethod
    def query_address(self, target: str, requester_node_id: str, requester_target: str):
        pass

    @abstractmethod
    def call_on_query_address_response(self, message: MessageAbstract, func: Callable[[str, Address], Any]) -> bool:
        pass
