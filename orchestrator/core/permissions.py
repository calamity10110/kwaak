
from __future__ import annotations

class PermissionManager:
    def __init__(self):
        self.decisions = {}
        self.session_rules = {}

    async def request(self, agent: str, resource: str, reversible: bool) -> bool:
        key = f"{agent}:{resource}"
        if key in self.decisions:
            return self.decisions[key]
        if reversible and key in self.session_rules:
            return self.session_rules[key]
        allow = True # TUI prompt here
        self.decisions[key] = allow
        if reversible:
            self.session_rules[key] = allow
        return allow
