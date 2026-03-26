import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any

import yaml

from enum import StrEnum


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    role: Role
    content: str
    tool_call_id: str | None = None
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "role": self.role,
            "content": self.content
        }
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.name:
            result["name"] = self.name
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result


@dataclass
class McpToolModel:
    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class SkillMetadata:
    name: str
    description: str
    skill_dir: Path
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    allowed_tools: Optional[list[str]] = None


_NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$')


def _validate(name: str, description: str, compatibility: Optional[str], dir_name: str) -> list[str]:
    errors: list[str] = []

    if not name:
        errors.append("name is empty")
    elif len(name) > 64:
        errors.append(f"name exceeds 64 chars ({len(name)})")
    elif not _NAME_RE.match(name):
        errors.append("name contains invalid characters or starts/ends with a hyphen")
    elif "--" in name:
        errors.append("name contains consecutive hyphens")

    if name != dir_name:
        errors.append(f"name '{name}' does not match directory name '{dir_name}'")

    if not description:
        errors.append("description is empty")
    elif len(description) > 1024:
        errors.append(f"description exceeds 1024 chars ({len(description)})")

    if compatibility is not None and len(compatibility) > 500:
        errors.append(f"compatibility exceeds 500 chars ({len(compatibility)})")

    return errors


def load_skills(skills_dir: Path) -> list[SkillMetadata]:
    """Load and validate all skills from the skills directory."""
    skills: list[SkillMetadata] = []

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(f"WARN: skipping '{skill_dir.name}' — no SKILL.md")
            continue

        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            print(f"WARN: skipping '{skill_dir.name}' — missing YAML frontmatter")
            continue

        try:
            end = content.index("---", 3)
            fm = yaml.safe_load(content[3:end]) or {}
        except Exception as e:
            print(f"WARN: skipping '{skill_dir.name}' — frontmatter parse error: {e}")
            continue

        name = str(fm.get("name", ""))
        description = str(fm.get("description", "")).strip()
        compatibility = str(fm["compatibility"]).strip() if fm.get("compatibility") else None

        errors = _validate(name, description, compatibility, skill_dir.name)
        if errors:
            print(f"WARN: skipping '{skill_dir.name}' — {'; '.join(errors)}")
            continue

        raw_at = fm.get("allowed-tools")
        if isinstance(raw_at, str):
            allowed_tools = raw_at.split() or None
        elif isinstance(raw_at, list):
            allowed_tools = raw_at or None
        else:
            allowed_tools = None

        skills.append(SkillMetadata(
            name=name,
            description=description,
            skill_dir=skill_dir,
            license=fm.get("license"),
            compatibility=compatibility,
            metadata=fm.get("metadata"),
            allowed_tools=allowed_tools,
        ))

    return skills
