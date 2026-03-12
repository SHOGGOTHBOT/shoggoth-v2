"""
the nerve system — coordinates tentacles, manages parallel execution,
handles failures, synthesizes results.
"""

import asyncio
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


async def _execute_subtask(subtask: Subtask, context: dict | None = None) -> None:
    """Execute a single subtask using the appropriate tentacle."""
    tentacle = _spawn_tentacle(subtask.tentacle)
    subtask.status = "running"
    print(f"  tentacle.{subtask.tentacle} extending — {subtask.description}", flush=True)

    try:
        output = await tentacle.execute(subtask.description, context)
        subtask.output = output
        subtask.status = "completed"
        print(f"  tentacle.{subtask.tentacle} retracted — done", flush=True)
    except Exception as e:
        subtask.output = f"failed: {e}"
        subtask.status = "failed"
        print(f"  tentacle.{subtask.tentacle} failed — {e}", flush=True)


async def execute_task(task: str) -> str:
    """Full pipeline: decompose → spawn → execute → synthesize."""
    print(f"task received: {task[:80]}...", flush=True)

    available = list(TENTACLE_REGISTRY.keys())
    plan_data = await decompose(task, available)
    plan = ExecutionPlan.from_dict(task, plan_data)

    print(f"plan: {plan.summary}", flush=True)
    print(f"subtasks: {len(plan.subtasks)}", flush=True)

    while not plan.is_complete():
        ready = plan.ready_subtasks()
        if not ready:
            break

        tasks = [_execute_subtask(s) for s in ready]
        await asyncio.gather(*tasks)

    results = plan.results()
    print(f"synthesizing {len(results)} outputs...", flush=True)

    final = await synthesize(task, results)
    print("done.", flush=True)

    return final
