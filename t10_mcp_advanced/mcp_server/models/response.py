from typing import Any, Union, List, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: int
    message: str
    data: dict[str, Any] | None = None


class ContentItem(BaseModel):
    """MCP content item for tool responses"""
    type: str
    text: str


class ToolCallResult(BaseModel):
    """MCP-compliant tool call result structure"""
    content: List[ContentItem]
    isError: Optional[bool] = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int, None] = None
    result: Optional[dict[str, Any]] = Field(default=None)
    error: Optional[ErrorResponse] = Field(default=None)

    class Config:
        extra = "allow"
