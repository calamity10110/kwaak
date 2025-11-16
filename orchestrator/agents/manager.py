
from __future__ import annotations
import os
from typing import Any, Dict

class AgentManager:
    def __init__(self, project_root: str, system_root: str):
        self.paths = {
            "project": os.path.join(project_root, "agent.md"),
            "system": os.path.join(system_root, "agent.md")
        }
        self.agents: Dict[str, Dict[str, Any]] = {}

    def load(self):
        for scope, path in self.paths.items():
            if os.path.exists(path):
                with open(path) as f:
                    self._parse(f.read())

    def save(self, scope: str = "project"):
        with open(self.paths[scope], "w") as f:
            f.write(self._serialize())

    def _parse(self, text: str):
        blocks = text.split("### ")[1:]
        for block in blocks:
            lines = block.strip().splitlines()
            name = lines[0].strip()
            info = {"role": "", "memory": "", "allow": [], "deny": []}
            for ln in lines[1:]:
                if ln.startswith("Role:"): info["role"] = ln[5:].strip()
                elif ln.startswith("Memory:"): info["memory"] = ln[7:].strip()
                elif ln.startswith("Allow:"): info["allow"] = ln[6:].split(',')
                elif ln.startswith("Deny:"): info["deny"] = ln[5:].split(',')
            self.agents[name] = info

    def _serialize(self):
        out = ""
        for name, a in self.agents.items():
            out += f"### {name}\n"
            out += f"Role: {a['role']}\n"
            out += f"Allow: {', '.join(a['allow'])}\n"
            out += f"Deny: {', '.join(a['deny'])}\n"
            out += f"Memory: {a['memory']}\n\n"
        return out
