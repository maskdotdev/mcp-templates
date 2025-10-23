"""
Tools that connect to the MCP server for ChromaDB operations.

This module wraps the MCP server's tools so they can be used by the ADK agent.
"""
import asyncio
import os
from typing import Any
from fastmcp import Client  # type: ignore


# Path to the MCP server script (relative to this file)
MCP_SERVER_PATH = os.path.join(os.path.dirname(__file__), "..", "server.py")

# Global client instance (initialized lazily)
_mcp_client = None
_client_context = None


async def _get_mcp_client():
    """Get or create the MCP client instance."""
    global _mcp_client, _client_context
    
    if _mcp_client is None:
        _client_context = Client(MCP_SERVER_PATH)
        _mcp_client = await _client_context.__aenter__()
    
    return _mcp_client


def _run_async(coro: Any) -> Any:
    """Helper to run async functions synchronously."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context
            import nest_asyncio  # type: ignore
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop exists, create a new one
        return asyncio.run(coro)


def search_documents(query: str, n_results: int = 5, collection: str = "documents") -> dict[str, Any]:
    """
    Searches for documents via the MCP server based on a query.

    Args:
        query (str): The search query to find relevant documents.
        n_results (int, optional): Maximum number of results to return. Defaults to 5.
        collection (str): Collection name (default: "documents").

    Returns:
        dict: status with found documents and their content, or error msg.
    """
    async def _search():
        client = await _get_mcp_client()
        result = await client.call_tool("search_documents", {
            "query": query,
            "max_results": n_results,
            "collection": collection
        })
        
        # Parse the MCP server's formatted response
        response_text = result.content[0].text
        
        # Return a structured response
        return {
            "status": "success",
            "message": f"Search completed for query: '{query}'",
            "results": response_text
        }
    
    try:
        return _run_async(_search())
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search documents: {str(e)}",
        }


def list_collections() -> dict[str, Any]:
    """
    Lists all available document collections via the MCP server.

    Returns:
        dict: status with collection names and counts.
    """
    async def _list():
        client = await _get_mcp_client()
        result = await client.call_tool("list_collections", {})
        return {"status": "success", "collections": result.content[0].text}
    
    try:
        return _run_async(_list())
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to list collections: {str(e)}"}


async def cleanup_mcp_client() -> None:
    """Clean up the MCP client connection. Call this when shutting down."""
    global _mcp_client, _client_context
    
    if _client_context is not None:
        try:
            await _client_context.__aexit__(None, None, None)
        except Exception:
            pass
        _mcp_client = None
        _client_context = None

