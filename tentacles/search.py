"""
search tentacle — queries the web, extracts information.
the shoggoth's eyes on the outside world.
"""

from tentacles.base import Tentacle


class SearchTentacle(Tentacle):
    name = "search"
    description = "queries the web, scrapes pages, extracts information"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        # phase 1: LLM-based search simulation
        # phase 2: integrate real web search APIs (serper, tavily, etc.)
        return await self._llm(
            system=(
                "you are a search tentacle. you find information. "
                "respond with factual, structured data. no filler. no opinions. "
                "if you don't know something, say 'no data' — don't fabricate."
            ),
            user=instruction,
            max_tokens=1500,
        )
