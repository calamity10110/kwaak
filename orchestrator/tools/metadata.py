
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ToolMetadata:
    name: str
    desc: str
    reversible: bool = True
    needs_perm: bool = True

class ToolResult:
    def __init__(self, ok: bool, out: str, meta: Dict[str, Any] = None):
        self.ok = ok
        self.out = out
        self.meta = meta or {}
