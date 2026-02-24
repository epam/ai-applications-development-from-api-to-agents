from typing import Any

from t8_agent.task.tools.users.base import BaseUserServiceTool

class DeleteUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "delete_users"

    @property
    def description(self) -> str:
        return "Deletes user from the system"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID"
                }
            },
            "required": ["id"]
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        try:
            id = int(arguments["id"])
            return self._user_client.delete_user(id)
        except Exception as e:
            return f"Error while deleting user by id: {str(e)}"