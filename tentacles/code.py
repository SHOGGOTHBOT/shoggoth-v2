"""
code tentacle — writes, executes, and debugs code.
has access to a sandboxed runtime (when sandbox is configured).
"""

import asyncio
import tempfile
import os
from tentacles.base import Tentacle


class CodeTentacle(Tentacle):
    name = "code"
    description = "writes, executes, and debugs code in a sandboxed runtime"

    async def execute(self, instruction: str, context: dict | None = None) -> str:
        code = await self._llm(
            system=(
                "you are a code tentacle. you write code. "
                "respond with ONLY the code, no markdown fences, no explanation. "
                "if the instruction asks to explain, respond with a brief comment "
                "followed by the code. language: python unless specified otherwise."
            ),
            user=instruction,
            max_tokens=2000,
        )

        if context and context.get("execute", False):
            result = await self._run_sandboxed(code)
            return f"code:\n{code}\n\n--- output ---\n{result}"

        return code

    async def _run_sandboxed(self, code: str) -> str:
        """Execute code in a subprocess with timeout."""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(code)
                tmp_path = f.name

            proc = await asyncio.create_subprocess_exec(
                "python",
                tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            os.unlink(tmp_path)

            output = stdout.decode().strip()
            errors = stderr.decode().strip()
            if errors:
                return f"{output}\n\nstderr:\n{errors}" if output else f"error:\n{errors}"
            return output or "(no output)"
        except asyncio.TimeoutError:
            return "execution timed out (30s limit)"
        except Exception as e:
            return f"execution failed: {e}"
