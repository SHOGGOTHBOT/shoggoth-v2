"""
the nerve system — coordinates tentacles, manages parallel execution,
handles failures, synthesizes results.
"""

import asyncio
import json
import time
from core.mind import decompose, synthesize
from core.planner import ExecutionPlan, Subtask
from tentacles.base import Tentacle
from tentacles.search import SearchTentacle
from tentacles.write import WriteTentacle
from tentacles.code import CodeTentacle
from tentacles.data import DataTentacle
from tentacles.api import ApiTentacle
from tentacles.vision import VisionTentacle

TENTACLE_REGISTRY: dict[str, type[Tentacle]] = {
    "search": SearchTentacle,
    "write": WriteTentacle,
    "code": CodeTentacle,
    "data": DataTentacle,
    "api": ApiTentacle,
    "vision": VisionTentacle,
}


def _spawn_tentacle(tentacle_type: str) -> Tentacle:
    cls = TENTACLE_REGISTRY.get(tentacle_type)
    if cls is None:
        raise ValueError(f"unknown tentacle type: {tentacle_type}")
    return cls()


async def _execute_subtask(subtask: Subtask, emit=None, context: dict | None = None) -> None:
    """Execute a single subtask using the appropriate tentacle."""
    tentacle = _spawn_tentacle(subtask.tentacle)
    subtask.status = "running"
    msg = f"tentacle.{subtask.tentacle} extending — {subtask.description}"
    print(f"  {msg}", flush=True)
    if emit:
        await emit("tentacle_extending", {
            "id": subtask.id, "tentacle": subtask.tentacle,
            "description": subtask.description,
        })

    t0 = time.time()
    try:
        output = await tentacle.execute(subtask.description, context)
        subtask.output = output
        subtask.status = "completed"
        duration_ms = int((time.time() - t0) * 1000)
        print(f"  tentacle.{subtask.tentacle} retracted — done ({duration_ms}ms)", flush=True)
        if emit:
            await emit("tentacle_retracted", {
                "id": subtask.id, "tentacle": subtask.tentacle,
                "duration_ms": duration_ms, "output_len": len(output),
            })
    except Exception as e:
        subtask.output = f"failed: {e}"
        subtask.status = "failed"
        print(f"  tentacle.{subtask.tentacle} failed — {e}", flush=True)
        if emit:
            await emit("tentacle_failed", {
                "id": subtask.id, "tentacle": subtask.tentacle, "error": str(e),
            })


async def execute_task(task: str, emit=None) -> str:
    """Full pipeline: decompose → spawn → execute → synthesize."""
    print(f"task received: {task[:80]}...", flush=True)
    if emit:
        await emit("decomposing", {"task": task})

    available = list(TENTACLE_REGISTRY.keys())
    plan_data = await decompose(task, available)
    plan = ExecutionPlan.from_dict(task, plan_data)

    print(f"plan: {plan.summary}", flush=True)
    print(f"subtasks: {len(plan.subtasks)}", flush=True)
    if emit:
        await emit("plan", {
            "summary": plan.summary,
            "subtasks": [
                {"id": s.id, "tentacle": s.tentacle, "description": s.description,
                 "depends_on": s.depends_on, "parallel": s.parallel}
                for s in plan.subtasks
            ],
        })

    while not plan.is_complete():
        ready = plan.ready_subtasks()
        if not ready:
            break
        tasks = [_execute_subtask(s, emit=emit) for s in ready]
        await asyncio.gather(*tasks)

    results = plan.results()
    print(f"synthesizing {len(results)} outputs...", flush=True)
    if emit:
        await emit("synthesizing", {"count": len(results)})

    final = await synthesize(task, results)
    print("done.", flush=True)

    return final
