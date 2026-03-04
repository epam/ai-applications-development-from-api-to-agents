import json
import anthropic
from pathlib import Path

from commons.constants import ANTHROPIC_API_KEY


SKILLS_VERSION = "skills-2025-10-02"

def get_or_create_skill(skill_title: str, skill_dir: Path,  client: anthropic.Anthropic) -> str:
    skills = client.beta.skills.list(source="custom", betas=[SKILLS_VERSION])
    print(skills)
    for skill in skills.data:
        print(skill.display_title)
        if skill.display_title == skill_title:
            print(f"Skill already exists: {skill.id} (latest version: {skill.latest_version})")
            return skill.id

    skill = client.beta.skills.create(
        display_title=skill_title,
        files=anthropic.lib.files_from_dir(str(skill_dir)),
        betas=[SKILLS_VERSION],
    )
    print(f"Skill uploaded: {skill.id}")
    return skill.id

def delete_skills(client: anthropic.Anthropic):
    skills = client.beta.skills.list(source="custom", betas=[SKILLS_VERSION])
    for skill in skills.data:
        versions = client.beta.skills.versions.list(skill.id, betas=[SKILLS_VERSION])
        for v in versions.data:
            client.beta.skills.versions.delete(v.version, skill_id=skill.id, betas=[SKILLS_VERSION])
            print(f"Deleted version {v.version} of {skill.display_title}")
        client.beta.skills.delete(skill_id=skill.id, betas=[SKILLS_VERSION])
        print(f"Deleted skill {skill.display_title}")

def chat(client: anthropic.Anthropic, skill_id: str, log_request: bool=True, log_response: bool = True):
    """Multi-turn chat loop that reuses the container across turns."""
    messages = []
    container_id = None
    print("\nStyle Guide Agent is ready. Ask it to write, rewrite, or review any text.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        container = {
            "skills": [
                {
                    "type": "custom",
                    "skill_id": skill_id,
                    "version": "latest"
                }
            ]
        }
        if container_id:
            container["id"] = container_id

        request_payload = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 4096,
            "messages": messages,
            "container": container,
            "betas": [
                "code-execution-2025-08-25",
                SKILLS_VERSION,
                # "files-api-2025-04-14"
            ],
            "tools": [
                {
                    "type": "code_execution_20250825",
                    "name": "code_execution"
                }
            ],
        }

        if log_request:
            print("\n--- REQUEST ---")
            print(json.dumps(request_payload, indent=2, default=str))
            print("---------------\n")


        response = client.beta.messages.create(**request_payload)

        if log_response:
            print("\n--- RESPONSE ---")
            print(json.dumps(response.model_dump(), indent=2, default=str))
            print("----------------\n")
        else:
            reply = " ".join(b.text for b in response.content if hasattr(b, "text"))
            print(f"\nClaude: {reply}\n")

        if hasattr(response, "container") and response.container:
            container_id = response.container.id

        messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )




STYLE_SKILL_TITLE = "style-guide"
STYLE_SKILL_DIR = Path(__file__).parent / "_skills" / STYLE_SKILL_TITLE

CALCULATOR_SKILL_TITLE = "calculator"
CALCULATOR_SKILL_DIR = Path(__file__).parent / "_skills" / CALCULATOR_SKILL_TITLE

def main():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    skill_id = get_or_create_skill(
        client=client,
        skill_dir=STYLE_SKILL_DIR,
        skill_title=STYLE_SKILL_TITLE
    )
    chat(client, skill_id)
    delete_skills(client)


if __name__ == "__main__":
    main()