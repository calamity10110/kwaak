
from __future__ import annotations
from typing import Any, Dict, Optional
from orchestrator.storage.db import StructuredDB

class SessionManager:
    def __init__(self, db: StructuredDB):
        self.db = db
        self.stack = []
        self.max = 10

    async def compress(self, agent: str, memory: str):
        compressed = memory[:200]
        self.stack.append({"agent": agent, "mem": compressed})
        if len(self.stack) > self.max:
            self.stack.pop(0)
        await self.db.add(f"{agent}_diff_{len(self.stack)}", compressed, [0.0] * 16)

    def undo(self) -> Optional[Dict[str, Any]]:
        return self.stack.pop() if self.stack else None
