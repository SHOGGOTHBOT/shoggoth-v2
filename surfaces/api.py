"""
REST API surface — raw endpoint for programmatic access.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


async def submit_task(request: Request, execute_fn):
    body = await request.json()
    task = body.get("task", "").strip()
    if not task:
        return JSONResponse({"error": "empty task"}, status_code=400)

    result = await execute_fn(task)
    return JSONResponse({"task": task, "result": result})
