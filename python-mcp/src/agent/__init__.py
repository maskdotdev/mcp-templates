"""Agent module for MCP-based document search."""

from .agent import document_agent
from .tools import cleanup_mcp_client

__all__ = ["document_agent", "cleanup_mcp_client"]

