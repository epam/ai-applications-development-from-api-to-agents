import asyncio
import xml.etree.ElementTree as ET
from pathlib import Path

from openai import OpenAI

from commons.constants import OPENAI_API_KEY
from commons.models.message import Message
from commons.models.role import Role
from t12_skills.custom.agent import T12Agent
from t12_skills.custom.tools.base import BaseTool
from t12_skills.custom.models import SkillMetadata, load_skills
from t12_skills.custom.tools.py_interpreter.python_code_interpreter_tool import PythonCodeInterpreterTool
from t12_skills.custom.tools.skills.read_skill_tool import ReadSkillTool

SKILLS_DIR = Path(__file__).parent / "_skills"
MCP_URL = "http://localhost:8050/mcp"
MCP_TOOL_NAME = "execute_code"

def _build_available_skills_xml(skills: list[SkillMetadata]) -> str:
    root = ET.Element("available_skills")
    for skill in skills:
        el = ET.SubElement(root, "skill", attrib={"name": skill.name})
        ET.SubElement(el, "description").text = skill.description
        if skill.license:
            ET.SubElement(el, "license").text = skill.license
        if skill.compatibility:
            ET.SubElement(el, "compatibility").text = skill.compatibility
        if skill.metadata:
            meta = ET.SubElement(el, "metadata")
            for k, v in skill.metadata.items():
                ET.SubElement(meta, k).text = str(v)
        if skill.allowed_tools:
            ET.SubElement(el, "allowed-tools").text = " ".join(skill.allowed_tools)
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode")


def build_system_prompt(skills: list[SkillMetadata]) -> str:
    return f"""\
You are an AI assistant with access to agent skills.

{_build_available_skills_xml(skills)}

## How to use skills

When the user's request matches a skill, activate it:
1. Call `read_skill` with the skill's SKILL.md path (e.g. path="/<skill-name>/SKILL.md") to load
   its full instructions.
2. Follow the instructions in the loaded SKILL.md precisely.
3. If the instructions reference additional files (scripts, references, assets), read them on demand
   using `read_skill` (e.g. path="/<skill-name>/scripts/calculate.py").
4. If the skill requires running a Python script, execute it with `{MCP_TOOL_NAME}`.

Always read the relevant SKILL.md before performing the task.\
"""


async def main():
    skills = load_skills(SKILLS_DIR)
    if not skills:
        print(f"ERROR: no valid skills found in {SKILLS_DIR}")
        return
    print(f"Loaded {len(skills)} skill(s): {[s.name for s in skills]}")

    system_prompt = build_system_prompt(skills)
    print(f"📄 System prompt: \n {system_prompt}")
    messages: list[Message] = [
        Message(
            role=Role.SYSTEM,
            content=system_prompt
        )
    ]

    tools: list[BaseTool] = [
        ReadSkillTool(skills_dir=SKILLS_DIR),
        await PythonCodeInterpreterTool.create(
            mcp_url=MCP_URL,
            tool_name=MCP_TOOL_NAME,
            skills_dir=SKILLS_DIR
        )
    ]

    agent = T12Agent(
        client=OpenAI(api_key=OPENAI_API_KEY),
        model="gpt-5.2",
        tools=tools
    )

    while True:
        user_input = input("➡️: ").strip()
        if user_input.lower() == "exit":
            break

        messages.append(
            Message(
                role=Role.USER,
                content=user_input
            )
        )

        assistant_message = await agent.chat_completion(
            messages = messages,
            log_messages=True,
        )
        messages.append(assistant_message)


if __name__ == "__main__":
    asyncio.run(main())
