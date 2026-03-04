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
    #TODO:
    # 1. Create XML root element: `root = ET.Element("available_skills")`
    # 2. For each `skill` in `skills`:
    #       a. Create sub-element: `el = ET.SubElement(root, "skill", attrib={"name": skill.name})`
    #       b. Add `<description>` sub-element with text `skill.description`
    #       c. If `skill.license`, add `<license>` sub-element with text `skill.license`
    #       d. If `skill.compatibility`, add `<compatibility>` sub-element with text `skill.compatibility`
    #       e. If `skill.metadata`, add `<metadata>` sub-element and for each k, v in its items
    #          add a child sub-element with tag=k and text=str(v)
    #       f. If `skill.allowed_tools`, add `<allowed-tools>` sub-element with text " ".join(skill.allowed_tools)
    # 3. Call `ET.indent(root, space="  ")`
    # 4. Return `ET.tostring(root, encoding="unicode")`
    raise NotImplementedError()


def build_system_prompt(skills: list[SkillMetadata]) -> str:
    #TODO:
    # 1. Call `_build_available_skills_xml(skills)` and embed in an f-string system prompt that:
    #    - Declares the agent as "an AI assistant with access to agent skills"
    #    - Embeds the available skills XML
    #    - Explains the "How to use skills" workflow:
    #      * Call `read_skill` with the skill's SKILL.md path to load its full instructions
    #      * Follow the instructions in the loaded SKILL.md precisely
    #      * If instructions reference additional files, read them using `read_skill`
    #      * If the skill requires running a Python script, execute it with `{MCP_TOOL_NAME}`
    #    - Ends with "Always read the relevant SKILL.md before performing the task."
    # 2. Return the prompt string
    raise NotImplementedError()


async def main():
    #TODO:
    # 1. Call `load_skills(SKILLS_DIR)`, assign to `skills`
    # 2. If not skills, print f"ERROR: no valid skills found in {SKILLS_DIR}" and return
    # 3. Print f"Loaded {len(skills)} skill(s): {[s.name for s in skills]}"
    # 4. Call `build_system_prompt(skills)`, assign to `system_prompt`;
    #    print f"📄 System prompt: \n {system_prompt}"
    # 5. Create `messages: list[Message] = [Message(role=Role.SYSTEM, content=system_prompt)]`
    # 6. Create `tools: list[BaseTool] = [ReadSkillTool(skills_dir=SKILLS_DIR), await PythonCodeInterpreterTool.create(mcp_url=MCP_URL, tool_name=MCP_TOOL_NAME, skills_dir=SKILLS_DIR)]`
    # 7. Create `agent = T12Agent(client=OpenAI(api_key=OPENAI_API_KEY), model="gpt-5.2", tools=tools)`
    # 8. Start while True loop: read input with `input("➡️: ").strip()`, break on "exit",
    #    append `Message(role=Role.USER, content=user_input)` to `messages`,
    #    await `agent.chat_completion(messages=messages, log_messages=True)`, assign to `assistant_message`,
    #    append `assistant_message` to `messages`
    raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(main())
