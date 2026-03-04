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
        #TODO: Return the tool name
        raise NotImplementedError()

    @property
    def description(self) -> str:
        #TODO: Return a description telling the agent when and how to use this tool
        #      (what it reads, what path format to use)
        raise NotImplementedError()

    @property
    def parameters(self) -> dict[str, Any]:
        #TODO: Return the JSON schema for the tool parameters
        #      Single required string parameter "path" with a description of the expected format
        raise NotImplementedError()

    async def _execute(self, arguments: dict[str, Any]) -> str:
        #TODO:
        # - Get the path from arguments and strip the leading "/"
        # - Resolve the full filesystem path by combining self._skills_dir with the relative path
        # - Return the file content using `get_file_content` method
        raise NotImplementedError()