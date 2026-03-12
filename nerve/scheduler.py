"""
task queue — manages incoming tasks and their execution order.
fifo for now. priority queue later.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class QueuedTask:
    id: str
    task: str
    submitted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "queued"  # queued | processing | completed | failed
    result: str | None = None


class TaskQueue:
    def __init__(self):
        self._queue: asyncio.Queue[QueuedTask] = asyncio.Queue()
        self._tasks: dict[str, QueuedTask] = {}

    async def submit(self, task_id: str, task_text: str) -> QueuedTask:
        qt = QueuedTask(id=task_id, task=task_text)
        self._tasks[task_id] = qt
        await self._queue.put(qt)
        return qt

    async def next(self) -> QueuedTask:
        return await self._queue.get()

    def get(self, task_id: str) -> QueuedTask | None:
        return self._tasks.get(task_id)

    def pending_count(self) -> int:
        return self._queue.qsize()
