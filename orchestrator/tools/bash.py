
from __future__ import annotations
import asyncio
from typing import Any, Dict
from orchestrator.tools.manager import Tool
from orchestrator.tools.metadata import ToolResult

class BashTool(Tool):
    def __init__(self, root: str):
        self.root = root

    async def call(self, payload: Dict[str, Any]) -> ToolResult:
        cmd = payload.get("cmd", "")
        if not cmd:
            return ToolResult(False, "no command")
        try:
            proc = await asyncio.create_subprocess_shell(cmd, cwd=self.root, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            out, err = await proc.communicate()
            txt = (out.decode() + err.decode()).strip()
            return ToolResult(proc.returncode == 0, txt, {"code": proc.returncode})
        except Exception as e:
            return ToolResult(False, str(e))
