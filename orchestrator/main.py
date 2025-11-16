
from __future__ import annotations
from typing import Any, Dict

from orchestrator.core.config import OrchestratorConfig
from orchestrator.llm.provider import LLMProvider, LocalLLMProvider
from orchestrator.llm.openai import OpenAIProvider
from orchestrator.storage.db import StructuredDB
from orchestrator.agents.manager import AgentManager
from orchestrator.tools.manager import ToolManager
from orchestrator.core.budget import TokenBudget
from orchestrator.core.session import SessionManager
from orchestrator.core.permissions import PermissionManager
from orchestrator.tools.bash import BashTool
from orchestrator.tools.metadata import ToolMetadata

class LLMOrchestrator:
    def __init__(self, cfg: OrchestratorConfig):
        self.cfg = cfg
        self.llm = self._init_llm_provider()
        self.db = StructuredDB("memory", cfg.project_root + "/db")
        self.agents = AgentManager(cfg.project_root, cfg.system_root)
        self.tools = ToolManager()
        self.tokens = TokenBudget(cfg.max_tokens)
        self.sessions = SessionManager(self.db)
        self.perms = PermissionManager()
        self._core_tools()

    def _init_llm_provider(self) -> LLMProvider:
        if self.cfg.llm_provider == "openai":
            return OpenAIProvider(**(self.cfg.provider_settings or {}))
        else:
            return LocalLLMProvider()

    def _core_tools(self):
        self.tools.register(
            "bash",
            BashTool(self.cfg.project_root),
            ToolMetadata(name="bash", desc="Execute project shell commands", reversible=False, needs_perm=True)
        )

    async def run(self, agent: str, prompt: str) -> Dict[str, Any]:
        if not await self.tokens.reserve(prompt):
            return {"error": "token limit"}

        # Embed the prompt and query the database for context
        prompt_embedding = await self.llm.embed(prompt)
        db_results = await self.db.query(prompt_embedding)

        # Format the context
        context = ""
        if db_results and db_results.get("documents"):
            context += "Relevant Information:\n"
            for doc in db_results["documents"][0]:
                context += f"- {doc}\n"

        # Prepend context to the prompt
        final_prompt = f"{context}\nUser's Request: {prompt}"

        a = self.agents.agents.get(agent)
        if not a:
            return {"error": "unknown agent"}
        await self.sessions.compress(agent, a.get("memory", ""))
        try:
            out = await self.llm.generate(final_prompt)
            return {"agent": agent, "reply": out}
        finally:
            await self.tokens.release(prompt)
