"""
api tentacle — calls external services.
twitter, telegram, discord, anything with an endpoint.
"""

from tentacles.base import Tentacle


class ApiTentacle(Tentacle):
    name = "api"
    description = "calls external APIs and services"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        # phase 1: plan the API call via LLM
        # phase 2: actually execute HTTP requests with httpx
        return await self._llm(
            system=(
                "you are an api tentacle. you interact with external services. "
                "given an instruction, describe the exact API call needed: "
                "method, endpoint, headers, body. format as structured output."
            ),
            user=instruction,
            max_tokens=1000,
        )
