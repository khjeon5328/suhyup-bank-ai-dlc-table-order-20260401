"""SSE connection manager — synced with Unit 1 (store_code based)."""

import json
from typing import AsyncGenerator, Optional

from app.core.event_bus import EventBus, SSEEvent, event_bus as default_event_bus


class SSEManager:
    def __init__(self, bus: Optional[EventBus] = None):
        self._event_bus = bus or default_event_bus

    async def stream_admin(self, store_code: str) -> AsyncGenerator[str, None]:
        queue = await self._event_bus.subscribe(store_code)
        try:
            while True:
                event: SSEEvent = await queue.get()
                yield self._format_sse(event)
        finally:
            self._event_bus.unsubscribe(store_code, queue)

    async def stream_table(self, store_code: str, table_no: int) -> AsyncGenerator[str, None]:
        queue = await self._event_bus.subscribe(store_code)
        try:
            while True:
                event: SSEEvent = await queue.get()
                if event.table_no == table_no or event.table_no is None:
                    yield self._format_sse(event)
        finally:
            self._event_bus.unsubscribe(store_code, queue)

    @staticmethod
    def _format_sse(event: SSEEvent) -> str:
        data = json.dumps(event.data, ensure_ascii=False, default=str)
        return f"event: {event.type}\ndata: {data}\n\n"


sse_manager = SSEManager()
