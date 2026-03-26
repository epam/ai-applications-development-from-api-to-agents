import json
import logging
import uuid
from datetime import datetime, UTC
from typing import Optional, AsyncGenerator

import redis.asyncio as redis

from t13_final_task.task.agent.models import Message
from t13_final_task.task.agent.models import Role
from t13_final_task.task.agent.ums_agent import UMSAgent

logger = logging.getLogger(__name__)

_CONVERSATION_PREFIX = "conversation:"
_CONVERSATION_LIST_KEY = "conversations:list"

class ConversationManager:
    """Manages conversation lifecycle including AI interactions and persistence"""

    def __init__(self, ums_agent: UMSAgent, redis_client: redis.Redis, system_prompt: str):
        self.ums_agent = ums_agent
        self.redis = redis_client
        self._system_prompt = system_prompt
        logger.info("ConversationManager initialized")

    async def create_conversation(self, title: str) -> dict:
        """Create a new conversation"""
        #TODO:
        # - Build conversation dict: id (uuid4), title, messages=[], created_at, updated_at (UTC ISO)
        # - Persist to Redis: set by key, zadd to sorted list with timestamp score
        # - Return conversation dict
        raise NotImplementedError()

    async def list_conversations(self) -> list[dict]:
        """List all conversations sorted by last update time"""
        #TODO:
        # - Get all conversation ids via zrevrange on _CONVERSATION_LIST_KEY
        # - For each id fetch from Redis, parse, append summary dict (id, title, created_at, updated_at, message_count)
        # - Return list of summaries
        raise NotImplementedError()

    async def get_conversation(self, conversation_id: str) -> Optional[dict]:
        """Get a specific conversation"""
        #TODO:
        # - Get from Redis by key, return None if missing
        # - Return parsed conversation dict
        raise NotImplementedError()

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        #TODO:
        # - Delete from Redis by key; return False if not found (deleted == 0)
        # - Remove from sorted list via zrem
        # - Return True
        raise NotImplementedError()

    async def chat(
            self,
            user_message: Message,
            conversation_id: str,
            stream: bool = False
    ):
        """
        Process chat messages and return AI response.
        Automatically saves conversation state.
        """

        #TODO:
        # - Load conversation via get_conversation(); raise ValueError if not found
        # - Deserialize messages; if empty inject system prompt (Role.SYSTEM) first
        # - Append user_message
        # - If stream: return self._stream_chat(...), else return await self._non_stream_chat(...)
        raise NotImplementedError()

    async def _stream_chat(
            self,
            conversation_id: str,
            messages: list[Message],
    ) -> AsyncGenerator[str, None]:
        """Handle streaming chat with automatic saving"""
        #TODO:
        # - Yield conversation_id as first SSE event
        # - Yield each chunk from ums_agent.stream_response(messages)
        # - Save messages via _save_conversation_messages()
        raise NotImplementedError()

    async def _non_stream_chat(
            self,
            conversation_id: str,
            messages: list[Message],
    ) -> dict:
        """Handle non-streaming chat"""
        #TODO:
        # - Get ai_message via ums_agent.response(messages)
        # - Save messages via _save_conversation_messages()
        # - Return dict with content and conversation_id
        raise NotImplementedError()

    async def _save_conversation_messages(
            self,
            conversation_id: str,
            messages: list[Message]
    ):
        """Save or update conversation messages"""
        #TODO:
        # - Fetch existing conversation from Redis, update messages (to_dict) and updated_at
        # - Persist via _save_conversation()
        raise NotImplementedError()

    async def _save_conversation(self, conversation: dict):
        """Internal method to persist conversation to Redis"""
        #TODO:
        # - redis.set conversation by key (json.dumps)
        # - redis.zadd to sorted list with current timestamp score
        raise NotImplementedError()
