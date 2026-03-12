"""
base tentacle — all tentacles inherit from this.
a tentacle is a disposable sub-agent spawned for one job.
"""

import os
from abc import ABC, abstractmethod
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_TENTACLE = os.getenv("MODEL_TENTACLE", "gpt-4o-mini")


class Tentacle(ABC):
    """Base class for all tentacles."""

    name: str = "base"
    description: str = "abstract tentacle"

    @abstractmethod
    async def execute(self, instruction: str, context: dict | None = None) -> str:
        """Execute the tentacle's task and return output."""
        ...

    async def _llm(self, system: str, user: str, max_tokens: int = 1000) -> str:
        response = await client.chat.completions.create(
            model=MODEL_TENTACLE,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def __repr__(self) -> str:
        return f"<Tentacle:{self.name}>"
