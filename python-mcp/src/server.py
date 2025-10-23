#!/usr/bin/env python3
"""
MCP Server for Document Search using ChromaDB.

Provides semantic document search capabilities via the Model Context Protocol.
"""

from fastmcp import FastMCP
import json
from pathlib import Path

# Create the MCP server
mcp = FastMCP("Document Search Server")


def _get_chroma_client():
    """Helper function to get ChromaDB client."""
    import chromadb
    db_path = Path(__file__).parent.parent / "chroma_db"
    return chromadb.PersistentClient(path=str(db_path))


@mcp.tool()
def search_documents(
    query: str,
    collection: str = "default",
    max_results: int = 5
) -> str:
    """
    Search through stored documents using semantic search.
    
    Args:
        query: The search query for semantic matching
        collection: The document collection to search in (default: "default")
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Matching documents with relevance scores and metadata
    """
    try:
        client = _get_chroma_client()
        
        # Get collection
        try:
            coll = client.get_collection(name=collection)
        except Exception:
            available = [c.name for c in client.list_collections()]
            return f"❌ Collection '{collection}' not found.\nAvailable collections: {available}"
        
        # Perform semantic search
        results = coll.query(
            query_texts=[query],
            n_results=max_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return f"No documents found matching query: '{query}'"
        
        # Format results
        formatted = [f"🔍 Search Results for: '{query}'\n"]
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0] if results['metadatas'] else [{}] * len(results['documents'][0]),
            results['distances'][0] if results['distances'] else [0] * len(results['documents'][0])
        ), 1):
            relevance = max(0, 1 - distance / 2)  # Convert distance to relevance score
            
            # Show full content or truncate
            content = doc if len(doc) <= 300 else f"{doc[:300]}..."
            
            formatted.append(
                f"\n{'='*60}\n"
                f"Result #{i} | Relevance: {relevance:.1%}\n"
                f"{'-'*60}\n"
                f"{content}\n"
            )
            
            if metadata:
                formatted.append(f"Metadata: {json.dumps(metadata, indent=2)}")
        
        return "".join(formatted)
        
    except ImportError:
        return "❌ ChromaDB not available. Install with: uv pip install chromadb"
    except Exception as e:
        return f"❌ Error searching documents: {str(e)}"


@mcp.tool()
def list_collections() -> str:
    """
    List all available document collections with statistics.
    
    Returns:
        List of collection names with document counts
    """
    try:
        client = _get_chroma_client()
        collections = client.list_collections()
        
        if not collections:
            return "📚 No collections found in the database.\n\nTip: Use add_document() to create your first collection and add documents."
        
        result = ["📚 Available Collections:\n"]
        for coll in collections:
            count = coll.count()
            result.append(f"  • {coll.name}: {count} document{'s' if count != 1 else ''}")
        
        return "\n".join(result)
        
    except ImportError:
        return "❌ ChromaDB not available. Install with: uv pip install chromadb"
    except Exception as e:
        return f"❌ Error listing collections: {str(e)}"




@mcp.resource("search://help")
def search_help() -> str:
    """
    Get help information about the document search server.
    """
    return """
# Document Search MCP Server Help

This server provides semantic document search using ChromaDB and FastMCP.

## Available Tools:

### Search Operations
- search_documents: Semantic search across documents
- get_document_by_id: Retrieve a specific document by ID

### Document Management
- add_document: Add a single document
- add_documents_batch: Add multiple documents at once
- delete_document: Remove a document by ID

### Collection Management
- list_collections: View all collections with document counts

## Learn More:
- FastMCP: https://github.com/jlowin/fastmcp
- ChromaDB: https://www.trychroma.com/
"""


if __name__ == "__main__":
    # Run the server
    # Default transport is STDIO (for local use)
    # Use transport="http" for web deployment
    mcp.run()

