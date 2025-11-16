
from __future__ import annotations
import asyncio
from typing import List
import chromadb

class StructuredDB:
    def __init__(self, name: str, persist_dir: str):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.col = self.client.get_or_create_collection(name=name)

    async def add(self, key: str, text: str, embedding: List[float]):
        await asyncio.get_event_loop().run_in_executor(None, lambda:
            self.col.add(ids=[key], documents=[text], embeddings=[embedding], metadatas=[{"id": key}])
        )

    async def query(self, embedding: List[float], n: int = 5):
        return await asyncio.get_event_loop().run_in_executor(None, lambda:
            self.col.query(query_embeddings=[embedding], n_results=n)
        )
