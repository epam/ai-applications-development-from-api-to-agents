from typing import Any

from commons.user_service.user_info import UserCreate
from t8_agent.task.tools.users.base import BaseUserServiceTool


class CreateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "add_user"

    @property
    def description(self) -> str:
        return "Adds new user"

    @property
    def input_schema(self) -> dict[str, Any]:
        return UserCreate.model_json_schema()

    def execute(self, arguments: dict[str, Any]) -> str:
        try:
            user = UserCreate.model_validate(arguments)
            return self._user_client.add_user(user)
        except Exception as e:
            return f"Error while creating a new user: {str(e)}"
