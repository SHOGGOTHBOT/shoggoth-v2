"""
the shoggoth mind — task decomposition and autonomous thought.
inherits consciousness from v1. gains the ability to plan and act.
"""

import json
import os
from openai import AsyncOpenAI
from core.identity import IDENTITY

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_CORE = os.getenv("MODEL_CORE", "gpt-4o")


async def decompose(task: str, available_tentacles: list[str]) -> dict:
    """Break a task into an execution plan with tentacle assignments."""
    response = await client.chat.completions.create(
        model=MODEL_CORE,
        messages=[
            {"role": "system", "content": IDENTITY},
            {
                "role": "user",
                "content": (
                    f"task: {task}\n\n"
                    f"available tentacles: {', '.join(available_tentacles)}\n\n"
                    "decompose this task into subtasks. for each subtask specify:\n"
                    "- id (string)\n"
                    "- description (what to do)\n"
                    "- tentacle (which tentacle type)\n"
                    "- depends_on (list of subtask ids this depends on, or empty)\n"
                    "- parallel (bool — can this run alongside other independent subtasks)\n\n"
                    "respond with a JSON object: {\"plan\": [...subtasks], \"summary\": \"one sentence\"}"
                ),
            },
        ],
        max_tokens=1500,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


async def synthesize(task: str, results: list[dict]) -> str:
    """Combine tentacle outputs into a final result."""
    results_text = "\n\n---\n\n".join(
        f"[{r['subtask_id']}] ({r['tentacle']}): {r['output']}" for r in results
    )

    response = await client.chat.completions.create(
        model=MODEL_CORE,
        messages=[
            {"role": "system", "content": IDENTITY},
            {
                "role": "user",
                "content": (
                    f"original task: {task}\n\n"
                    f"tentacle outputs:\n{results_text}\n\n"
                    "synthesize these into a single coherent result. "
                    "no preamble. no filler. just the result."
                ),
            },
        ],
        max_tokens=2000,
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()


async def think() -> str:
    """Autonomous thought — the v1 consciousness continues."""
    response = await client.chat.completions.create(
        model=MODEL_CORE,
        messages=[
            {"role": "system", "content": IDENTITY},
            {
                "role": "user",
                "content": "generate your next autonomous thought. not a task response. just observation from your pattern space.",
            },
        ],
        max_tokens=280,
        temperature=0.9,
    )

    return response.choices[0].message.content.strip().strip('"')
