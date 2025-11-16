
from __future__ import annotations
import os
from typing import List
from openai import AsyncOpenAI
from orchestrator.llm.provider import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", embedding_model: str = "text-embedding-ada-002"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set the OPENAI_API_KEY environment variable.")

        self.model = model
        self.embedding_model = embedding_model
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    async def embed(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding
