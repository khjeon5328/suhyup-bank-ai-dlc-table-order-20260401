"""Tests for EventBus — store_code based."""

import pytest
from app.core.event_bus import EventBus, SSEEvent


@pytest.mark.asyncio
class TestEventBus:
    async def test_publish_and_subscribe(self):
        bus = EventBus()
        queue = await bus.subscribe(store_code="TEST01")
        event = SSEEvent(type="order_created", data={"id": 1}, store_code="TEST01", table_no=1)
        await bus.publish(event)
        received = queue.get_nowait()
        assert received.type == "order_created"

    async def test_store_isolation(self):
        bus = EventBus()
        q1 = await bus.subscribe(store_code="TEST01")
        q2 = await bus.subscribe(store_code="TEST02")
        await bus.publish(SSEEvent(type="test", data={}, store_code="TEST01"))
        assert not q1.empty()
        assert q2.empty()

    async def test_unsubscribe(self):
        bus = EventBus()
        queue = await bus.subscribe(store_code="TEST01")
        bus.unsubscribe(store_code="TEST01", queue=queue)
        await bus.publish(SSEEvent(type="test", data={}, store_code="TEST01"))
        assert queue.empty()
