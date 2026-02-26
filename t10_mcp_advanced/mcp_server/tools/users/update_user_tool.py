from typing import Any

from commons.user_service.user_info import UserUpdate
from t10_mcp_advanced.mcp_server.tools.users.base import BaseUserServiceTool


class UpdateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "update_user"

    @property
    def description(self) -> str:
        return "Updates user info"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be updated."
                },
                "new_info": UserUpdate.model_json_schema()
            },
            "required": ["id"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_id = arguments["id"]
        user = UserUpdate.model_validate(arguments["new_info"])
        return self._user_client.update_user(user_id, user)
