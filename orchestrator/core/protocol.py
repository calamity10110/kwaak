
from __future__ import annotations
from typing import Any, Dict
import msgpack

class CompactProtocol:
    @staticmethod
    def encode(obj: Dict[str, Any]) -> bytes:
        return msgpack.packb(obj, use_bin_type=True)

    @staticmethod
    def decode(packed: bytes) -> Dict[str, Any]:
        return msgpack.unpackb(packed, raw=False)
