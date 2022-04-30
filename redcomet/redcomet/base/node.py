from abc import ABC, abstractmethod

from redcomet.actor.abstract import ActorAbstract
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.cluster.ref import ClusterRefAbstract
from redcomet.base.messaging.address import Address
from redcomet.base.messaging.inbox import Inbox
from redcomet.base.messaging.outbox import Outbox
from redcomet.base.messenger.messenger import MessengerAbstract


class NodeAbstract(ABC):

    @property
    @abstractmethod
    def discovery(self) -> Address:
        pass

    @abstractmethod
    def bind_discovery(self, address: Address):
        pass

    @abstractmethod
    def issue_actor_ref(self, local_issuer_id: str, ref_id: str) -> ActorRefAbstract:
        pass

    @abstractmethod
    def issue_cluster_ref(self, local_issuer_id: str) -> ClusterRefAbstract:
        pass

    @abstractmethod
    def register_executable_actor(self, actor: ActorAbstract, actor_id: str):
        pass

    @abstractmethod
    def assign_node_id(self, node_id: str):
        pass

    @property
    @abstractmethod
    def node_id(self) -> str:
        pass

    @property
    @abstractmethod
    def messenger(self) -> MessengerAbstract:
        pass

    @property
    @abstractmethod
    def outbox(self) -> Outbox:
        pass

    @property
    @abstractmethod
    def inbox(self) -> Inbox:
        pass

    @abstractmethod
    def make_connection_with(self, node: 'NodeAbstract'):
        pass

    @abstractmethod
    def make_connection_to(self, node: 'NodeAbstract'):
        pass
