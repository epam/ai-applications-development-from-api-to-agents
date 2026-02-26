from abc import ABC

from commons.user_service.client import UserServiceClient
from t10_mcp_advanced.mcp_server.tools.base import BaseTool


class BaseUserServiceTool(BaseTool, ABC):

    def __init__(self, user_client: UserServiceClient):
        super().__init__()
        self._user_client = user_client
