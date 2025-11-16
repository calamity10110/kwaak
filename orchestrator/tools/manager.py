
from __future__ import annotations
from typing import Any, Dict
from orchestrator.tools.metadata import ToolMetadata, ToolResult

class Tool:
    async def call(self, payload: Dict[str, Any]) -> ToolResult:
        raise NotImplementedError

class ToolManager:
    def __init__(self):
        self.tools = {}
        self.meta = {}

    def register(self, name: str, tool: Tool, meta: ToolMetadata):
        self.tools[name] = tool
        self.meta[name] = meta

    async def call(self, name: str, payload: Dict[str, Any]) -> ToolResult:
        return await self.tools[name].call(payload)
