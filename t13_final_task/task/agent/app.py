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

from t13_final_task.task.agent.clients.http_mcp_client import HttpMcpClient
from t13_final_task.task.agent.clients.stdio_mcp_client import StdioMcpClient
from t13_final_task.task.agent.conversation_manager import ConversationManager
from t13_final_task.task.agent.tools.base import BaseTool
from t13_final_task.task.agent.tools.mcp_tool import McpTool
from t13_final_task.task.agent.tools.read_skill_tool import ReadSkillTool
from t13_final_task.task.agent.ums_agent import UMSAgent
from t13_final_task.task.agent.models import SkillMetadata, load_skills, Message

SKILLS_DIR = Path(__file__).parent.parent / "_skills"


def _build_available_skills_xml(skills: list[SkillMetadata]) -> str:
    #TODO:
    # Build and return an XML string with root element <available_skills>.
    # For each skill add a <skill name="..."> element with child elements:
    #   - <description> (always)
    #   - <license> (if present)
    #   - <compatibility> (if present)
    #   - <metadata> with a dynamic child element per key/value pair (if present)
    #   - <allowed-tools> as a space-joined string (if present)
    raise NotImplementedError()


def build_system_prompt(skills: list[SkillMetadata]) -> str:
    #TODO:
    # Build and return the system prompt string that:
    #   - Describes the assistant as an AI with access to agent skills
    #   - Embeds the XML from _build_available_skills_xml(skills)
    #   - Explains how to use skills:
    #       1. Call `read_skill` with path="/<skill-name>/SKILL.md" to load instructions
    #       2. Follow the loaded SKILL.md precisely
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
    # 1. Load skills from SKILLS_DIR with load_skills(), build system_prompt with build_system_prompt()
    # 2. Create tools list starting with ReadSkillTool(skills_dir=SKILLS_DIR)
    # 3. Init HttpMcpClient via HttpMcpClient.create() using http://localhost:8005/mcp URL, get its tools and append each as McpTool
    # 4. Init StdioMcpClient with docker_image: "khshanovskyi/ddg-mcp-server:latest" get its tools and append each as McpTool
    # 5. Create UMSAgent
    # 6. Create redis.Redis client and ping it
    # 7. Create ConversationManager
    #    and assign to global conversation_manager

    yield

    #TODO: shutdown — close redis_client


app = FastAPI(
    #TODO: add `lifespan` param from above
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

#TODO:
# Create such endpoints:
# 1. POST: "/conversations". Applies CreateConversationRequest and creates new conversation with ConversationManager.
# 2. GET: "/conversations" Extracts all conversation from storage. Returns list of ConversationSummary objects
# 3. GET: "/conversations/{conversation_id}". Applies conversation_id string and extracts from storage full conversation
# 4. DELETE: "/conversations/{conversation_id}". Applies conversation_id string and deletes conversation. Returns dict
#    with message with info if conversation has been deleted
# 5. POST: "/conversations/{conversation_id}/chat". Chat endpoint that processes messages and returns assistant response.
#    Supports both streaming and non-streaming modes.
#    Applies conversation_id and ChatRequest.
#    If `request.stream` then return `StreamingResponse(result, media_type="text/event-stream")`, otherwise return `ChatResponse(**result)`



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server")
    uvicorn.run(
        #TODO:
        #  - app
        #  - host="0.0.0.0"
        #  - port=8011
        #  - log_level="debug"
    )