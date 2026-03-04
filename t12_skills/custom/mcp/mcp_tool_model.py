from typing import Any

from pydantic import BaseModel


class MCPToolModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
