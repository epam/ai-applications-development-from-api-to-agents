from pathlib import Path
from typing import Any

from t12_skills.custom.file_utils import get_file_content
from t12_skills.custom.tools.base import BaseTool


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
            "Paths are relative to the skills root, e.g. /calculator/SKILL.md "
            "or /calculator/scripts/calculate.py"
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
                        "E.g. /calculator/SKILL.md or /calculator/scripts/calculate.py"
                    ),
                }
            },
            "required": ["path"],
        }

    async def _execute(self, arguments: dict[str, Any]) -> str:
        raw_path = arguments["path"].lstrip("/")
        full_path = (self._skills_dir / raw_path).resolve()

        return get_file_content(full_path)