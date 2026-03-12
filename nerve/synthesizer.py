"""
result synthesizer — combines tentacle outputs.
delegates to core mind for final assembly.
"""

from core.mind import synthesize


async def combine(task: str, results: list[dict]) -> str:
    """Combine multiple tentacle outputs into a coherent result."""
    if len(results) == 1:
        return results[0].get("output", "")
    return await synthesize(task, results)
