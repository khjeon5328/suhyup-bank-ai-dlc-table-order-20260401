"""In-memory event bus — synced with Unit 1 (store_code based)."""

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SSEEvent:
    type: str
    data: Dict[str, Any]
    store_code: str
    table_no: Optional[int] = None


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)

    async def publish(self, event: SSEEvent) -> None:
        for queue in self._subscribers.get(event.store_code, []):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass

    async def subscribe(self, store_code: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._subscribers[store_code].append(queue)
        return queue

    def unsubscribe(self, store_code: str, queue: asyncio.Queue) -> None:
        queues = self._subscribers.get(store_code, [])
        if queue in queues:
            queues.remove(queue)


event_bus = EventBus()
