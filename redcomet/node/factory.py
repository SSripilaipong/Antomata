from redcomet.actor.executor import ActorExecutor
from redcomet.base.node.abstract import NodeAbstract
from redcomet.messenger.factory import create_messenger
from redcomet.node.manager.actor import NodeManager
from redcomet.node.process import ProcessNode
from redcomet.node.synchronous import SynchronousNode


def create_node(parallel: bool = False) -> NodeAbstract:
    executor = ActorExecutor()
    messenger = create_messenger(executor, actor_id="messenger", parallel=parallel)
    if not parallel:
        node = SynchronousNode(executor, messenger)
    else:
        node = ProcessNode(messenger, executor)
    executor.set_node(node)

    manager = NodeManager("manager", node)
    node.assign_manager(manager)

    executor.register("messenger", messenger)
    executor.register("manager", manager)

    return node
