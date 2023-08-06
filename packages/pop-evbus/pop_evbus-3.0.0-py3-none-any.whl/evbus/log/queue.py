import asyncio
import logging.handlers
import queue


def wrapper(hub, **kwargs):
    class AsyncQueueWrapper:
        def __init__(self):
            self.wait_queue = queue.Queue(**kwargs)

        @property
        def _loop(self) -> asyncio.AbstractEventLoop:
            return hub.pop.loop.CURRENT_LOOP

        @property
        def _queue(self) -> asyncio.Queue:
            return hub.ingress.QUEUE

        def put_nowait(self, record):
            if self._queue is None:
                # The asynchronous ingress queue has not yet been initialized, put it on the waiter
                self.wait_queue.put(record)
                return
            else:
                # If we got this far, clear the waiter queue onto the real one
                while not self.wait_queue.empty():
                    self.put_nowait(self.wait_queue.get())

            # Put new records onto the queue
            if self._loop is None:
                # No loop but we have a queue? put it on the queue immediately
                self._queue.put_nowait(record)
            else:
                # There is a loop and a queue, create a task
                coro = self._queue.put(record)
                self._loop.create_task(coro)

    return AsyncQueueWrapper()


def setup(hub, conf):
    """
    Log to the ingress queue
    """
    root = logging.getLogger()

    raw_level = conf["log_level"].strip().lower()
    if raw_level.isdigit():
        hub.log.INT_LEVEL = int(raw_level)
    else:
        hub.log.INT_LEVEL = hub.log.LEVEL.get(raw_level, root.level)

    root.setLevel(hub.log.INT_LEVEL)
    cf = logging.Formatter(fmt=conf["log_fmt_console"], datefmt=conf["log_datefmt"])
    ch = logging.StreamHandler()
    ch.setLevel(hub.log.INT_LEVEL)
    ch.setFormatter(cf)
    root.addHandler(ch)

    ff = logging.Formatter(fmt=conf["log_fmt_logfile"], datefmt=conf["log_datefmt"])
    _, kwargs = hub.render.cli.args(conf["log_handler_options"])

    qh = logging.handlers.QueueHandler(hub.log.queue.wrapper(**kwargs))
    qh.setLevel(hub.log.INT_LEVEL)
    qh.setFormatter(ff)
    root.addHandler(qh)
