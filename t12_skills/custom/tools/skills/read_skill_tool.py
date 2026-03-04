from pathlib import Path
from typing import Any

from t12_skills.custom.file_utils import get_file_content
from t12_skills.custom.tools.base import BaseTool


class ReadSkillTool(BaseTool):
    """Reads files from the local skills directory by path."""

    def __init__(self, skills_dir: Path):
        #TODO: Resolve `skills_dir` and assign to `self._skills_dir`
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return "read_skill"

    @property
    def description(self) -> str:
        #TODO: Return a string describing the tool — it reads a skill file by path,
        # used to access skill instructions, scripts, references, or any other skill resource;
        # paths are relative to the skills root, e.g. /calculator/SKILL.md or /calculator/scripts/calculate.py
        raise NotImplementedError()

    @property
    def parameters(self) -> dict[str, Any]:
        #TODO: Return a dict with:
        # - "type": "object"
        # - "properties": {"path": {"type": "string", "description": "Path to the skill file relative to the skills root. E.g. /calculator/SKILL.md or /calculator/scripts/calculate.py"}}
        # - "required": ["path"]
        raise NotImplementedError()

    async def _execute(self, arguments: dict[str, Any]) -> str:
        #TODO:
        # 1. Strip leading "/" from `arguments["path"]`, assign to `raw_path`
        # 2. Resolve the full path: `(self._skills_dir / raw_path).resolve()`, assign to `full_path`
        # 3. Return `get_file_content(full_path)`
        raise NotImplementedError()