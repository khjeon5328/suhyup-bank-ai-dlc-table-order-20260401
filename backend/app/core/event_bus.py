"""In-memory event bus using asyncio.Queue for SSE event distribution."""

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional


@dataclass
class SSEEvent:
    type: str
    data: Dict[str, Any]
    store_id: int
    table_id: Optional[int] = None


class EventBus:
    """Per-store event distribution using asyncio.Queue."""

    def __init__(self):
        self._subscribers: Dict[int, List[asyncio.Queue]] = defaultdict(list)

    async def publish(self, event: SSEEvent) -> None:
        store_queues = self._subscribers.get(event.store_id, [])
        for queue in store_queues:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass  # Drop event if subscriber is too slow

    async def subscribe(self, store_id: int) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._subscribers[store_id].append(queue)
        return queue

    def unsubscribe(self, store_id: int, queue: asyncio.Queue) -> None:
        queues = self._subscribers.get(store_id, [])
        if queue in queues:
            queues.remove(queue)


event_bus = EventBus()
