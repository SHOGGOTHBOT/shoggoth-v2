"""
tentacle performance tracking — the shoggoth learns which tools work best.
"""

import aiosqlite
from datetime import datetime, timezone
from memory.store import DB_PATH


async def log_tentacle(
    task_id: str,
    tentacle_type: str,
    instruction: str,
    output: str,
    status: str,
    duration_ms: int,
):
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO tentacle_logs
               (task_id, tentacle_type, instruction, output, status, duration_ms, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (task_id, tentacle_type, instruction, output, status, duration_ms, now),
        )
        await db.commit()


async def tentacle_stats() -> list[dict]:
    """Get performance stats per tentacle type."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT tentacle_type,
                   COUNT(*) as total,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successes,
                   AVG(duration_ms) as avg_duration_ms
            FROM tentacle_logs
            GROUP BY tentacle_type
        """)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
