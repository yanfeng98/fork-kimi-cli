import asyncio

from kimi_cli.utils.aioqueue import Queue


class BroadcastQueue[T]:
    def __init__(self) -> None:
        self._queues: set[Queue[T]] = set()

    def subscribe(self) -> Queue[T]:
        queue: Queue[T] = Queue()
        self._queues.add(queue)
        return queue

    def unsubscribe(self, queue: Queue[T]) -> None:
        """Remove a subscription queue."""
        self._queues.discard(queue)

    async def publish(self, item: T) -> None:
        """Publish an item to all subscription queues."""
        await asyncio.gather(*(queue.put(item) for queue in self._queues))

    def publish_nowait(self, item: T) -> None:
        for queue in self._queues:
            queue.put_nowait(item)

    def shutdown(self, immediate: bool = False) -> None:
        """Close all subscription queues."""
        for queue in self._queues:
            queue.shutdown(immediate=immediate)
        self._queues.clear()
