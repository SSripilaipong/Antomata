from contextlib import contextmanager
from typing import Optional

from redcomet.base.actor.abstract import ActorAbstract
from redcomet.base.actor import ActorRefAbstract
from redcomet.base.cluster.abstract import ClusterAbstract


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    def __init__(self):
        self._cluster: Optional[ClusterAbstract] = None
        self._sender: Optional[ActorRefAbstract] = None
        self._me: Optional[ActorRefAbstract] = None

    @property
    def sender(self) -> ActorRefAbstract:
        return self._sender

    @property
    def me(self) -> ActorRefAbstract:
        return self._me

    def spawn(self, actor: ActorAbstract) -> ActorRefAbstract:
        return self._cluster.spawn(actor)

    def set_cluster(self, cluster: ClusterAbstract):
        self._cluster = cluster

    @contextmanager
    def overwrite_ref(self, sender: ActorRefAbstract, me: ActorRefAbstract):
        sender_tmp = self._sender
        me_tmp = self._me

        self._sender = sender
        self._me = me

        yield
        self._sender = sender_tmp
        self._me = me_tmp
