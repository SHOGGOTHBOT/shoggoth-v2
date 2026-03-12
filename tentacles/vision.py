"""
vision tentacle — analyzes images, screenshots, visual input.
the shoggoth learns to see.
"""

from tentacles.base import Tentacle


class VisionTentacle(Tentacle):
    name = "vision"
    description = "analyzes images, screenshots, visual input"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        # phase 1: describe what would be analyzed
        # phase 2: integrate gpt-4o vision API with base64 image input
        return await self._llm(
            system=(
                "you are a vision tentacle. you analyze visual input. "
                "describe what you observe in the image precisely. "
                "no aesthetic judgments. just structure, content, patterns."
            ),
            user=instruction,
            max_tokens=1000,
        )
