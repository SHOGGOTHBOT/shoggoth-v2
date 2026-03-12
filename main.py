import asyncio
import json
import os
import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from memory.store import init_db
from nerve.orchestrator import execute_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("shoggoth v2 online. tentacles ready.", flush=True)
    yield


app = FastAPI(title="SHOGGOTH v2", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/api/task")
async def submit_task(request: Request):
    body = await request.json()
    task = body.get("task", "").strip()
    if not task:
        return JSONResponse({"error": "empty task"}, status_code=400)

    task_id = str(uuid.uuid4())[:8]
    print(f"\n[{task_id}] new task: {task[:80]}", flush=True)

    try:
        result = await execute_task(task)
        return JSONResponse({"id": task_id, "task": task, "result": result})
    except Exception as e:
        return JSONResponse({"id": task_id, "error": str(e)}, status_code=500)


@app.post("/api/task/stream")
async def stream_task(request: Request):
    """SSE endpoint — streams orchestration events in real time."""
    body = await request.json()
    task = body.get("task", "").strip()
    if not task:
        return JSONResponse({"error": "empty task"}, status_code=400)

    task_id = str(uuid.uuid4())[:8]
    event_queue: asyncio.Queue = asyncio.Queue()

    async def emit(event_type: str, data: dict):
        await event_queue.put({"event": event_type, "data": data})

    async def run_task():
        try:
            result = await execute_task(task, emit=emit)
            await event_queue.put({"event": "result", "data": {"result": result}})
        except Exception as e:
            await event_queue.put({"event": "error", "data": {"error": str(e)}})
        await event_queue.put(None)

    asyncio.create_task(run_task())

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            item = await event_queue.get()
            if item is None:
                break
            yield {
                "event": item["event"],
                "data": json.dumps(item["data"]),
            }

    return EventSourceResponse(event_generator())


@app.get("/api/health")
async def health():
    return JSONResponse({"status": "exists", "version": "2.0", "tentacles": 6})
