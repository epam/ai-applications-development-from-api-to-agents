from pathlib import Path
from typing import Any

from t13_final_task.task.agent.tools.base import BaseTool


class ReadSkillTool(BaseTool):
    """Reads files from the local skills directory by path."""

    def __init__(self, skills_dir: Path):
        self._skills_dir = skills_dir.resolve()

    @property
    def name(self) -> str:
        return "read_skill"

    @property
    def description(self) -> str:
        return (
            "Read a skill file by its path. Use this to access skill instructions, "
            "scripts, references, or any other skill resource. "
            "Paths are relative to the skills root, e.g. /sample/SKILL.md "
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Path to the skill file relative to the skills root. "
                        "E.g. /sample/SKILL.md"
                    ),
                }
            },
            "required": ["path"],
        }

    async def _execute(self, arguments: dict[str, Any]) -> str:
        #TODO:
        # 1. Strip leading `/` from `arguments["path"]` with `.lstrip("/")`
        # 2. Resolve the full path by joining `self._skills_dir` with the stripped path and calling `.resolve()`
        # 3. If the path does not exist, return an error string indicating the file was not found
        # 4. If the path is not a file (e.g. a directory), return an error string indicating it is not a file
        # 5. Return the file contents via `.read_text(encoding="utf-8")`
        raise NotImplementedError()
