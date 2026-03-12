"""
task memory — stores completed tasks and their outcomes.
the shoggoth remembers what it has done.
"""

import aiosqlite
import json
from datetime import datetime, timezone
from memory.store import DB_PATH


async def save_task(task_id: str, input_text: str, plan: dict, result: str, status: str):
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO tasks (id, input, plan, result, status, created_at, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (task_id, input_text, json.dumps(plan), result, status, now, now),
        )
        await db.commit()


async def get_task(task_id: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def recent_tasks(limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
