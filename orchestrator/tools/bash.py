
from __future__ import annotations
import asyncio
from typing import Any, Dict
from orchestrator.tools.manager import Tool
from orchestrator.tools.metadata import ToolResult
from orchestrator.core.feedback import ConsoleFeedback

class BashTool(Tool):
    def __init__(self, root: str):
        self.root = root
        self.feedback = ConsoleFeedback()

    async def call(self, payload: Dict[str, Any]) -> ToolResult:
        cmd = payload.get("cmd", "")
        if not cmd:
            return ToolResult(False, "no command")

        self.feedback.start_spinner(f"Running command: {cmd}")
        try:
            proc = await asyncio.create_subprocess_shell(cmd, cwd=self.root, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            out, err = await proc.communicate()
            txt = (out.decode() + err.decode()).strip()

            if proc.returncode == 0:
                self.feedback.stop_spinner(True, f"Command finished: {cmd}")
                return ToolResult(True, txt, {"code": proc.returncode})
            else:
                self.feedback.stop_spinner(False, f"Command failed: {cmd}")
                return ToolResult(False, txt, {"code": proc.returncode})
        except Exception as e:
            self.feedback.stop_spinner(False, f"Command failed with an exception: {cmd}")
            return ToolResult(False, str(e))
