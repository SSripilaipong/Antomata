from multiprocessing import Queue

from redcomet.queue.abstract import QueueAbstract


class DefaultQueue(Queue, QueueAbstract):
    pass
