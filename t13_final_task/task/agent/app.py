import logging
import os
import sys
import xml.etree.ElementTree as ET
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from task.agent.clients.http_mcp_client import HttpMcpClient
from task.agent.clients.stdio_mcp_client import StdioMcpClient
from task.agent.conversation_manager import ConversationManager
from task.agent.tools.base import BaseTool
from task.agent.tools.mcp_tool import McpTool
from task.agent.tools.read_skill_tool import ReadSkillTool
from task.agent.ums_agent import UMSAgent
from task.agent.models import SkillMetadata, load_skills, Message

SKILLS_DIR = Path(__file__).parent.parent / "_skills"


def _build_available_skills_xml(skills: list[SkillMetadata]) -> str:
    #TODO:
    # 1. Create the root XML element `<available_skills>` using `ET.Element`
    # 2. For each skill in the list, create a child `<skill>` element with attribute `name=skill.name`
    #    using `ET.SubElement`, then add child elements:
    #    - `<description>` — always present, set its `.text` to `skill.description`
    #    - `<license>`       — only if `skill.license` is set
    #    - `<compatibility>` — only if `skill.compatibility` is set
    #    - `<metadata>`      — only if `skill.metadata` is set; for each key/value pair inside,
    #                          create a child element named after the key with `.text = str(value)`
    #    - `<allowed-tools>` — only if `skill.allowed_tools` is set; join the list with spaces as text
    # 3. Call `ET.indent(root, space="  ")` to pretty-print the tree
    # 4. Return `ET.tostring(root, encoding="unicode")`
    raise NotImplementedError()


def build_system_prompt(skills: list[SkillMetadata]) -> str:
    #TODO:
    # Build and return the system prompt string using an f-string. It must contain:
    # 1. A role description line — state the assistant is an AI with access to agent skills
    # 2. The XML block produced by `_build_available_skills_xml(skills)` embedded inline
    # 3. A "How to use skills" section explaining:
    #    - When a user request matches a skill, call `read_skill` with the path "/<skill-name>/SKILL.md"
    #      to load its full instructions, then follow them precisely
    #    - Always read the relevant SKILL.md before performing the task
    raise NotImplementedError()


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

conversation_manager: Optional[ConversationManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize MCP clients, Redis, and ConversationManager on startup"""
    global conversation_manager

    #TODO:
    # Startup:
    # 1. Load skills from `SKILLS_DIR` using `load_skills()`, then build `system_prompt` with `build_system_prompt()`
    # 2. Create the tools list starting with `ReadSkillTool(skills_dir=SKILLS_DIR)`
    # 3. Init the UMS MCP client: read `UMS_MCP_URL` env var (default `"http://localhost:8005/mcp"`),
    #    create `HttpMcpClient` via its `create()` factory, then call `get_tools()` and wrap each
    #    result in a `McpTool(client=..., mcp_tool_model=...)` appended to the tools list
    # 4. Init the DuckDuckGo MCP client: create `StdioMcpClient` via its `create()` factory with
    #    `docker_image="khshanovskyi/ddg-mcp-server:latest"`, then do the same get_tools / McpTool wrapping
    # 5. Create `UMSAgent` with `api_key` from `OPENAI_API_KEY` env var, a `model` name, and `tools`
    # 6. Create `redis.Redis` with `host` from `REDIS_HOST` env var (default `"localhost"`) and
    #    `port` from `REDIS_PORT` env var (default `6379`), with `decode_responses=True`, then `ping()` it
    # 7. Create `ConversationManager(agent, redis_client, system_prompt=system_prompt)` and assign
    #    it to the global `conversation_manager`

    yield

    # Shutdown:
    # 8. Close `redis_client`


app = FastAPI(
    #TODO: add `lifespan` param from above, like:
    # - lifespan=lifespan
)
app.add_middleware(
    #TODO:
    # Since we will run it locally there will be some issues from FrontEnd side with CORS, and its okay for local setup to disable them:
    #   - CORSMiddleware,
    #   - allow_origins=["*"]
    #   - allow_credentials=True
    #   - allow_methods=["*"]
    #   - allow_headers=["*"]
)


# Request/Response Models
class ChatRequest(BaseModel):
    message: Message
    stream: bool = True


class ChatResponse(BaseModel):
    content: str
    conversation_id: str


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int


class CreateConversationRequest(BaseModel):
    title: str = None


# Endpoints
@app.get("/health")
async def health():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "conversation_manager_initialized": conversation_manager is not None
    }


@app.post("/conversations")
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation"""
    #TODO:
    # 1. Check if `conversation_manager` is present, if not then raise HTTPException(status_code=503, detail="Service not initialized")
    # 2. return result of `conversation_manager` create conversation with request title (it is async, don't forget about await)
    raise NotImplementedError()


@app.get("/conversations")
async def list_conversations():
    """List all conversations sorted by last update time"""
    #TODO:
    # 1. Check if `conversation_manager` is present, if not then raise HTTPException(status_code=503, detail="Service not initialized")
    # 2. Get conversations list with `conversation_manager` (it is async, don't forget about await)
    # 3. Converts dicts to `ConversationSummary` (iterate through it and create `ConversationSummary(**conv_dict)`) and return the result
    raise NotImplementedError()


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    #TODO:
    # 1. Check if `conversation_manager` is present, if not raise HTTPException(status_code=503, detail="Service not initialized")
    # 2. Fetch the conversation from `conversation_manager` using `conversation_id` (async)
    # 3. If the result is None, raise HTTPException(status_code=404, detail="Conversation not found")
    # 4. Return the conversation
    raise NotImplementedError()


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    #TODO:
    # 1. Check if `conversation_manager` is present, if not raise HTTPException(status_code=503, detail="Service not initialized")
    # 2. Call `conversation_manager.delete_conversation(conversation_id)` (async) and store the result
    # 3. If the result is falsy (conversation not found), raise HTTPException(status_code=404, detail="Conversation not found")
    # 4. Return a dict with a `message` key confirming successful deletion
    raise NotImplementedError()


@app.post("/conversations/{conversation_id}/chat")
async def chat(conversation_id: str, request: ChatRequest):
    """
    Chat endpoint that processes messages and returns assistant response.
    Supports both streaming and non-streaming modes.
    Automatically saves conversation state.
    """
    #TODO:
    # 1. Check if `conversation_manager` is present, if not raise HTTPException(status_code=503, detail="Service not initialized")
    # 2. Call `conversation_manager.chat(user_message=request.message, conversation_id=conversation_id, stream=request.stream)` (async)
    #    and store the result
    # 3. If `request.stream` is True, return `StreamingResponse(result, media_type="text/event-stream")`
    # 4. Otherwise return `ChatResponse(**result)`
    raise NotImplementedError()


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8011,
        log_level="debug",
    )