from redcomet.actor.executor import ActorExecutor
from redcomet.base.node.abstract import NodeAbstract
from redcomet.messaging.handler import PacketHandler
from redcomet.messenger.factory import create_messenger
from redcomet.node.manager import NodeManager
from redcomet.node.process import ProcessNode
from redcomet.node.synchronous import SynchronousNode


def create_node(parallel=False) -> NodeAbstract:
    executor = ActorExecutor()
    if not parallel:
        messenger = create_messenger(PacketHandler(executor), actor_id="messenger")
        node = SynchronousNode(executor, messenger)
    else:
        messenger = create_messenger(PacketHandler(executor), actor_id="messenger", parallel=True)
        node = ProcessNode()
    executor.set_node(node)

    manager = NodeManager("manager", node)
    node._manager = manager

    executor.register("messenger", messenger)
    executor.register("manager", manager)

    return node
