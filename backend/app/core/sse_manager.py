"""SSE connection manager with event filtering."""

import json
from typing import AsyncGenerator, Optional

from app.core.event_bus import EventBus, SSEEvent, event_bus as default_event_bus


class SSEManager:
    def __init__(self, bus: Optional[EventBus] = None):
        self._event_bus = bus or default_event_bus

    async def stream_admin(self, store_id: int) -> AsyncGenerator[str, None]:
        """Admin SSE stream — receives all store events."""
        queue = await self._event_bus.subscribe(store_id)
        try:
            while True:
                event: SSEEvent = await queue.get()
                yield self._format_sse(event)
        finally:
            self._event_bus.unsubscribe(store_id, queue)

    async def stream_table(
        self, store_id: int, table_id: int
    ) -> AsyncGenerator[str, None]:
        """Table SSE stream — receives only events for this table."""
        queue = await self._event_bus.subscribe(store_id)
        try:
            while True:
                event: SSEEvent = await queue.get()
                if event.table_id == table_id or event.table_id is None:
                    yield self._format_sse(event)
        finally:
            self._event_bus.unsubscribe(store_id, queue)

    @staticmethod
    def _format_sse(event: SSEEvent) -> str:
        data = json.dumps(event.data, ensure_ascii=False, default=str)
        return f"event: {event.type}\ndata: {data}\n\n"


sse_manager = SSEManager()
