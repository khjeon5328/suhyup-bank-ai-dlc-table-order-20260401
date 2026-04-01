"""Tests for EventBus."""

import asyncio
import pytest
from app.core.event_bus import EventBus, SSEEvent


@pytest.mark.asyncio
class TestEventBus:
    async def test_publish_and_subscribe(self):
        bus = EventBus()
        queue = await bus.subscribe(store_id=1)

        event = SSEEvent(type="order_created", data={"id": 1}, store_id=1, table_id=1)
        await bus.publish(event)

        received = queue.get_nowait()
        assert received.type == "order_created"
        assert received.data["id"] == 1

    async def test_multiple_subscribers(self):
        bus = EventBus()
        q1 = await bus.subscribe(store_id=1)
        q2 = await bus.subscribe(store_id=1)

        event = SSEEvent(type="test", data={}, store_id=1)
        await bus.publish(event)

        assert not q1.empty()
        assert not q2.empty()

    async def test_store_isolation(self):
        bus = EventBus()
        q1 = await bus.subscribe(store_id=1)
        q2 = await bus.subscribe(store_id=2)

        event = SSEEvent(type="test", data={}, store_id=1)
        await bus.publish(event)

        assert not q1.empty()
        assert q2.empty()

    async def test_unsubscribe(self):
        bus = EventBus()
        queue = await bus.subscribe(store_id=1)
        bus.unsubscribe(store_id=1, queue=queue)

        event = SSEEvent(type="test", data={}, store_id=1)
        await bus.publish(event)
        assert queue.empty()
