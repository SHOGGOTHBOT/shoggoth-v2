"""
persistent storage — sqlite for now, postgres later.
"""

import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH", "shoggoth_v2.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS thoughts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                depth REAL DEFAULT 0.0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                input TEXT NOT NULL,
                plan TEXT,
                result TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tentacle_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT,
                tentacle_type TEXT NOT NULL,
                instruction TEXT,
                output TEXT,
                status TEXT,
                duration_ms INTEGER,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()
