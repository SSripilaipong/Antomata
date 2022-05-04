from multiprocessing import Manager


class ProcessSafeQueue:
    def __enter__(self):
        self._manager = Manager()
        self._queue = self._manager.Queue()
        return self._queue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._manager.shutdown()
