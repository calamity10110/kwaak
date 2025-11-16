
from __future__ import annotations
import os
import json
from orchestrator.main import LLMOrchestrator

class ProjectInitializer:
    def __init__(self, orchestrator: LLMOrchestrator):
        self.orch = orchestrator
        self.root = orchestrator.cfg.project_root
        self.agent_file = os.path.join(self.root, "agent.md")
        self.meta_key = "project_metadata"

    async def init(self):
        files = self._scan()
        meta = {
            "project_root": self.root,
            "file_count": len(files),
            "files": files[:50],
        }
        emb = await self.orch.llm.embed(json.dumps(meta))
        await self.orch.db.add(self.meta_key, json.dumps(meta), emb)
        self._ensure_agent_md()
        await self.orch.sessions.compress("system", json.dumps(meta))
        return meta

    def _scan(self):
        out = []
        for base, _, files in os.walk(self.root):
            for f in files:
                p = os.path.join(base, f)
                if "/db/" not in p:
                    out.append(os.path.relpath(p, self.root))
        return out

    def _ensure_agent_md(self):
        if not os.path.exists(self.agent_file):
            with open(self.agent_file, "w") as f:
                f.write("""### project_pri
Role: primary
Allow: bash
Deny:
Memory: initialized
""")
