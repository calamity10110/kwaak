
from __future__ import annotations
import asyncio

class TokenBudget:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.used = 0
        self.energy_mwh = 0.0
        self.lock = asyncio.Lock()

    def estimate(self, text: str) -> int:
        return max(1, len(text) // 4)

    async def reserve(self, text: str) -> bool:
        t = self.estimate(text)
        async with self.lock:
            if self.used + t > self.max_tokens:
                return False
            self.used += t
            self.energy_mwh += t * 0.00003
            return True

    async def release(self, text: str):
        t = self.estimate(text)
        async with self.lock:
            self.used = max(0, self.used - t)
