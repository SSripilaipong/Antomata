from redcomet.actor.executor import ActorExecutor
from redcomet.messaging.handler import PacketHandler
from redcomet.messenger.factory import create_messenger
from redcomet.node.manager import NodeManager
from redcomet.node.synchronous import Node


def create_node(executor: ActorExecutor) -> Node:

    messenger = create_messenger(PacketHandler(executor), actor_id="messenger")
    node = Node(executor, messenger)
    executor.set_node(node)

    manager = NodeManager("manager", node)
    node._manager = manager

    executor.register("messenger", messenger)
    executor.register("manager", manager)

    return node
