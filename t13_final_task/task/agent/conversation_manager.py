import json
import logging
import uuid
from datetime import datetime, UTC
from typing import Optional, AsyncGenerator

import redis.asyncio as redis

from task.agent.models import Message
from task.agent.models import Role
from task.agent.ums_agent import UMSAgent

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
        # 1. Generate a new `conversation_id` using `uuid.uuid4()` (convert to str)
        # 2. Capture the current UTC time as an ISO string using `datetime.now(UTC).isoformat()`
        # 3. Build the conversation dict with keys: `id`, `title`, `messages` (empty list),
        #    `created_at`, `updated_at` (both set to the timestamp from step 2)
        # 4. Persist to Redis: call `self.redis.set(...)` with key `_CONVERSATION_PREFIX + conversation_id`
        #    and value `json.dumps(conversation)` (async)
        # 5. Add to the sorted set: call `self.redis.zadd(...)` on `_CONVERSATION_LIST_KEY` with
        #    `{conversation_id: datetime.now(UTC).timestamp()}` as the score mapping (async)
        # 6. Return the conversation dict
        raise NotImplementedError()

    async def list_conversations(self) -> list[dict]:
        """List all conversations sorted by last update time"""
        #TODO:
        # 1. Fetch all conversation IDs sorted by score descending using
        #    `self.redis.zrevrange(_CONVERSATION_LIST_KEY, 0, -1)` (async)
        # 2. For each ID, fetch raw data from Redis with key `_CONVERSATION_PREFIX + conv_id` (async)
        # 3. If data exists, parse it with `json.loads` and append a summary dict to the result list:
        #    keys are `id`, `title`, `created_at`, `updated_at`, and `message_count` (len of messages list)
        # 4. Return the list of summary dicts
        raise NotImplementedError()

    async def get_conversation(self, conversation_id: str) -> Optional[dict]:
        """Get a specific conversation"""
        #TODO:
        # 1. Fetch raw data from Redis with key `_CONVERSATION_PREFIX + conversation_id` (async)
        # 2. If nothing returned, return `None`
        # 3. Parse with `json.loads` and return the conversation dict
        raise NotImplementedError()

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        #TODO:
        # 1. Delete the key `_CONVERSATION_PREFIX + conversation_id` from Redis using `self.redis.delete(...)` (async)
        # 2. If the return value is 0 (key didn't exist), return `False`
        # 3. Remove the ID from the sorted set via `self.redis.zrem(_CONVERSATION_LIST_KEY, conversation_id)` (async)
        # 4. Return `True`
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
        logger.info(
            "Processing chat request",
            extra={
                "conversation_id": conversation_id,
                "stream": stream,
                "message_role": user_message.role
            }
        )

        #TODO:
        # 1. Load the conversation via `self.get_conversation(conversation_id)` (async);
        #    if not found, raise `ValueError(f"Conversation with id {conversation_id} not found")`
        # 2. Deserialize the stored messages: build a list of `Message(**msg)` from `conversation["messages"]`
        # 3. If the messages list is empty (first turn), prepend a system message:
        #    `Message(role=Role.SYSTEM, content=self._system_prompt)`
        # 4. Append `user_message` to the messages list
        # 5. If `stream` is True, return `self._stream_chat(conversation_id, messages)` (not awaited — it's an async generator)
        #    Otherwise return `await self._non_stream_chat(conversation_id, messages)`
        raise NotImplementedError()

    async def _stream_chat(
            self,
            conversation_id: str,
            messages: list[Message],
    ) -> AsyncGenerator[str, None]:
        """Handle streaming chat with automatic saving"""
        logger.debug("Starting streaming chat", extra={"conversation_id": conversation_id})

        #TODO:
        # 1. Yield the conversation_id as the first SSE event:
        #    `f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"`
        # 2. Iterate `self.ums_agent.stream_response(messages)` with `async for` and yield each chunk
        # 3. After the stream ends, call `self._save_conversation_messages(conversation_id, messages)` (async)

    async def _non_stream_chat(
            self,
            conversation_id: str,
            messages: list[Message],
    ) -> dict:
        """Handle non-streaming chat"""
        logger.debug("Starting non-streaming chat", extra={"conversation_id": conversation_id})

        #TODO:
        # 1. Get the AI response via `await self.ums_agent.response(messages)` and store it as `ai_message`
        # 2. Save the updated messages via `await self._save_conversation_messages(conversation_id, messages)`
        # 3. Return a dict with keys `content` (use `ai_message.content or ""`) and `conversation_id`
        raise NotImplementedError()

    async def _save_conversation_messages(
            self,
            conversation_id: str,
            messages: list[Message]
    ):
        """Save or update conversation messages"""
        logger.debug(
            "Saving conversation messages",
            extra={"conversation_id": conversation_id}
        )

        #TODO:
        # 1. Fetch the existing conversation from Redis with key `_CONVERSATION_PREFIX + conversation_id` (async)
        #    and parse it with `json.loads`
        # 2. Replace `conversation["messages"]` with `[msg.to_dict() for msg in messages]`
        # 3. Update `conversation["updated_at"]` to `datetime.now(UTC).isoformat()`
        # 4. Persist the updated conversation via `await self._save_conversation(conversation)`
        raise NotImplementedError()

    async def _save_conversation(self, conversation: dict):
        """Internal method to persist conversation to Redis"""
        #TODO:
        # 1. Extract `conversation_id` from `conversation["id"]`
        # 2. Persist to Redis: `self.redis.set(...)` with key `_CONVERSATION_PREFIX + conversation_id`
        #    and value `json.dumps(conversation)` (async)
        # 3. Update the sorted set: `self.redis.zadd(_CONVERSATION_LIST_KEY, {conversation_id: datetime.now(UTC).timestamp()})` (async)
        raise NotImplementedError()
