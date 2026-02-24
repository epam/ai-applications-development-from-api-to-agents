from abc import ABC

from commons.user_service.client import UserServiceClient
from t8_agent.task.tools.base import BaseTool


class BaseUserServiceTool(BaseTool, ABC):
    """Base class for tools that interact with the User Service.

    Extends ``BaseTool`` with a shared ``UserServiceClient`` instance so every
    concrete tool (get, search, create, update, delete) can reach the service
    without wiring the client themselves.
    """

    def __init__(self, user_client: UserServiceClient):
        """Initialise the tool with a User Service client.

        Args:
            user_client: Pre-configured client for the User Service REST API.
                Shared across all tool calls for the lifetime of the agent.
        """
        super().__init__()
        self._user_client = user_client
