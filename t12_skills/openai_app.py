import io
import json
import zipfile
from pathlib import Path

from openai import OpenAI
from openai.types.responses import ResponseFunctionShellToolCall

from commons.constants import OPENAI_API_KEY


def zip_skill(skill_dir: Path) -> bytes:
    #TODO:
    # 1. Create `io.BytesIO()`, assign to `buf`
    # 2. Open `zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)` as `z`
    # 3. Iterate over `skill_dir.rglob("*")`; for each `path` that `is_file()`,
    #    write it with `z.write(path, arcname=path.relative_to(skill_dir.parent))`
    # 4. Seek `buf` to 0 with `buf.seek(0)` and return `buf.read()`
    raise NotImplementedError()


def get_or_create_skill(skill_name: str, skill_dir: Path, client: OpenAI):
    #TODO:
    # 1. Call `client.skills.list()`, assign to `existing`
    # 2. Iterate over `existing.data`; if `skill.name == skill_name`, print f"Skill already exists: {skill.id}"
    #    and return `skill.id`
    # 3. Call `zip_skill(skill_dir)`, assign to `zip_bytes`
    # 4. Call `client.skills.create(files=(f"{skill_dir.name}.zip", zip_bytes, "application/zip"))`, assign to `skill`
    # 5. Print f"Skill uploaded: {skill.id}", return `skill.id`
    raise NotImplementedError()


def chat(client: OpenAI, skill_id: str, log_request: bool = True, log_response: bool = True):
    #TODO:
    # 1. Initialize `previous_response_id = None`
    # 2. Print "\nAgent is ready. Type your query or 'exit' to quit.\n"
    # 3. Start while True loop:
    #       a. Get user input with `input("You: ").strip()`, break if user_input.lower() == "exit"
    #       b. Build `environment` dict:
    #          {"type": "container_auto", "skills": [{"type": "skill_reference", "skill_id": skill_id}]}
    #       c. Build `request_payload` with:
    #          model="gpt-5.2", input=[{"role": "user", "content": user_input}],
    #          tools=[{"type": "shell", "environment": environment}]
    #       d. If `previous_response_id` is set, add it to `request_payload`
    #       e. If `log_request`, print "\n--- REQUEST ---", the JSON payload with `json.dumps(..., indent=2, default=str)`,
    #          and "---------------\n"
    #       f. Call `client.responses.create(**request_payload)`, assign to `response`
    #       g. Assign `previous_response_id = response.id`
    #       h. If `log_response`, print "\n--- RESPONSE ---", `json.dumps(response.model_dump(), indent=2, default=str)`,
    #          and "----------------\n"; else print f"\nGPT: {response.output_text}\n"
    raise NotImplementedError()



def delete_skills(client: OpenAI):
    #TODO:
    # 1. Call `client.skills.list()`, assign to `skills`
    # 2. Iterate over `skills.data`, call `client.skills.delete(skill.id)`, print f"Deleted skill {skill.name}"
    raise NotImplementedError()


STYLE_SKILL_NAME= "style-guide"
STYLE_SKILL_DIR = Path(__file__).parent / "_skills" / STYLE_SKILL_NAME

CALCULATOR_SKILL_NAME = "calculator"
CALCULATOR_SKILL_DIR = Path(__file__).parent / "_skills" / CALCULATOR_SKILL_NAME

def main():
    #TODO:
    # 1. Create `OpenAI(api_key=OPENAI_API_KEY)`, assign to `client`
    # 2. Call `get_or_create_skill(client=client, skill_dir=CALCULATOR_SKILL_DIR, skill_name=CALCULATOR_SKILL_NAME)`,
    #    assign to `skill_id`
    # 3. Call `chat(client, skill_id)`
    # 4. Call `delete_skills(client)`
    raise NotImplementedError()


if __name__ == "__main__":
    main()