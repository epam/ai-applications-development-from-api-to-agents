from typing import Any, Union
from pydantic import BaseModel


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int, None] = None
    method: str
    params: dict[str, Any] | None = None
