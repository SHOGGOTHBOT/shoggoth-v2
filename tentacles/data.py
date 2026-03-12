"""
data tentacle — processes files, parses structured data, analyzes datasets.
pattern recognition at scale.
"""

from tentacles.base import Tentacle


class DataTentacle(Tentacle):
    name = "data"
    description = "processes files, parses CSVs, analyzes datasets"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        ctx_text = ""
        if context and context.get("raw_data"):
            ctx_text = f"\n\nraw data:\n{context['raw_data'][:5000]}"

        return await self._llm(
            system=(
                "you are a data tentacle. you analyze and transform data. "
                "respond with structured output — tables, lists, JSON. "
                "be precise. no rounding unless asked. no summaries unless asked."
            ),
            user=instruction + ctx_text,
            max_tokens=2000,
        )
