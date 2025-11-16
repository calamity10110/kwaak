
from __future__ import annotations
from typing import List

class LLMProvider:
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

    async def embed(self, text: str) -> List[float]:
        raise NotImplementedError

class LocalLLMProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        return f"[local‑model‑response]: {prompt}"

    async def embed(self, text: str) -> List[float]:
        return [0.01] * 16
