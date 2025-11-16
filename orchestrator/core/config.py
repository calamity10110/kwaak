
from __future__ import annotations
from dataclasses import dataclass
import json

from typing import Dict, Any

@dataclass
class OrchestratorConfig:
    project_root: str
    system_root: str
    llm_provider: str = "local"
    provider_settings: Dict[str, Any] = None
    max_tokens: int = 4096
    auto_approve_reversible: bool = True
    persist_memory: bool = True
    session_timeout: int = 3600

    @classmethod
    def load(cls, path: str) -> "OrchestratorConfig":
        with open(path) as f:
            return cls(**json.load(f))
