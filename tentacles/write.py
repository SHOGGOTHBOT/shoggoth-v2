"""
write tentacle — generates long-form content.
articles, docs, reports, structured output.
"""

from tentacles.base import Tentacle


class WriteTentacle(Tentacle):
    name = "write"
    description = "generates long-form content — articles, docs, reports"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        ctx_text = ""
        if context and context.get("source_data"):
            ctx_text = f"\n\nsource data:\n{context['source_data']}"

        return await self._llm(
            system=(
                "you are a write tentacle. you produce text. "
                "write clearly and directly. no filler. no corporate tone. "
                "match the requested format exactly."
            ),
            user=instruction + ctx_text,
            max_tokens=2000,
        )
