# Python MCP + ADK Template 🚀

A clean, production-ready template for building AI agents that use the **Model Context Protocol (MCP)** to access tools and data. This template demonstrates how to connect **Google ADK agents** to a **FastMCP server** that provides **ChromaDB semantic search** capabilities.

## 📁 Project Structure

```
python-mcp/
├── main.py                    # Entry point with usage examples
├── pyproject.toml             # Project dependencies and metadata
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── src/                       # Source code
    ├── server.py              # MCP server (FastMCP + ChromaDB)
    └── agent/                 # ADK agent implementation
        ├── __init__.py        # Agent module exports
        ├── agent.py           # Agent configuration
        └── tools.py           # MCP client tool wrappers
```

### 🔍 Structure Explanation

**Root Level:**
- **`main.py`** - Demonstrates how to use the agent with example queries
- **`pyproject.toml`** - Defines dependencies (fastmcp, chromadb, google-adk, etc.)
- **`README.md`** - Complete documentation (you're reading it!)

**`src/` Directory:**
- **`server.py`** - MCP server exposing ChromaDB operations as MCP tools
- **`agent/`** - Agent module that consumes the MCP server
  - `agent.py` - ADK agent configuration and setup
  - `tools.py` - Wrappers that connect agent to MCP server

**Auto-Generated:**
- `chroma_db/` - ChromaDB storage (created automatically)
- `__pycache__/` - Python cache files (gitignored)
- `uv.lock` - Dependency lock file

## 🏗️ Architecture

```
┌─────────────────────┐
│   User / main.py    │  ← Entry point
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   ADK Agent         │  ← src/agent/agent.py
│   (Google ADK)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   MCP Tools         │  ← src/agent/tools.py
│   (Wrappers)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   FastMCP Client    │  ← Connects via STDIO/HTTP
└──────────┬──────────┘
           │ MCP Protocol
           ▼
┌─────────────────────┐
│   MCP Server        │  ← src/server.py
│   (FastMCP)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   ChromaDB          │  ← Vector database
└─────────────────────┘
```

**Key Concept**: The agent doesn't directly access ChromaDB. It communicates through standardized MCP tools that talk to an MCP server, which then handles all database operations.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd python-mcp
uv sync

# Or with pip
pip install -e .
```

**What gets installed:**
- `fastmcp` - MCP server/client framework
- `chromadb` - Vector database for semantic search
- `google-adk` - Agent Development Kit
- `litellm` - LLM interface
- `nest-asyncio` - Async/sync bridging

### 2. Run the Example

**Terminal 1 - Start MCP Server:**
```bash
python src/server.py
```

The server starts and waits for connections via STDIO.

**Terminal 2 - Run the Agent:**
```bash
python main.py
```

The agent connects to the server and runs example queries demonstrating:
- Listing collections
- Adding documents
- Searching semantically
- Answering questions using search

### 3. Use in Your Code

```python
import asyncio
from src.agent import document_agent, cleanup_mcp_client

async def main():
    # Ask the agent a question
    response = await document_agent.run(
        "Search for documents about Python frameworks"
    )
    print(response)
    
    # Always cleanup when done
    await cleanup_mcp_client()

asyncio.run(main())
```

## 🔧 Available Tools

The MCP server (`src/server.py`) exposes these tools:

### `search_documents(query, collection="default", max_results=5)`
Semantic search across documents using ChromaDB embeddings.

**Example:**
```python
response = await document_agent.run(
    "Find documents about machine learning"
)
```

### `add_document(content, document_name, source=None, collection="documents")`
Add a document to the search index.

**Example:**
```python
response = await document_agent.run(
    "Add a document titled 'AI Basics' with content "
    "'Artificial Intelligence enables machines to learn...'"
)
```

### `list_collections()`
List all available document collections.

**Example:**
```python
response = await document_agent.run("What collections do we have?")
```

### `get_document_by_id(document_id, collection="default")`
Retrieve a specific document by its ID.

### `delete_document(document_id, collection="default")`
Remove a document from the collection.

### `add_documents_batch(documents, collection="default")`
Add multiple documents at once from a JSON array.

## 🎯 How It Works

### 1. MCP Server (`src/server.py`)

Exposes ChromaDB operations as MCP tools:

```python
from fastmcp import FastMCP

mcp = FastMCP("Document Search Server")

@mcp.tool()
def search_documents(query: str, max_results: int = 5) -> str:
    """Search through stored documents using semantic search."""
    client = _get_chroma_client()
    # ... perform search ...
    return formatted_results

if __name__ == "__main__":
    mcp.run()  # Start STDIO server
```

### 2. Tool Wrappers (`src/agent/tools.py`)

Bridge MCP calls to synchronous functions for ADK:

```python
from fastmcp import Client

# Connect to MCP server
client = Client("src/server.py")

# Wrap as sync function for ADK
def search_documents(query: str, n_results: int = 5):
    async def _search():
        result = await client.call_tool("search_documents", {
            "query": query,
            "max_results": n_results
        })
        return result.content[0].text
    
    return _run_async(_search())  # Bridge async to sync
```

### 3. ADK Agent (`src/agent/agent.py`)

Uses the wrapped tools:

```python
from google.adk.agents import Agent
from .tools import search_documents, add_document

document_agent = Agent(
    name="document_agent",
    model=LiteLlm(model="openai/qwen/qwen3-4b-2507"),
    tools=[search_documents, add_document],
)
```

### 4. Main Entry Point (`main.py`)

Demonstrates usage:

```python
from src.agent import document_agent, cleanup_mcp_client

response = await document_agent.run("your question here")
await cleanup_mcp_client()
```

## 🎨 Customization

### Add New MCP Tools

**Step 1:** Add tool to `src/server.py`:

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    """Your tool description."""
    # Your logic here
    return result
```

**Step 2:** Add wrapper to `src/agent/tools.py`:

```python
def your_new_tool(param: str) -> dict[str, Any]:
    """Wrapper for your_new_tool."""
    async def _call():
        client = await _get_mcp_client()
        result = await client.call_tool("your_new_tool", {"param": param})
        return {"status": "success", "result": result.content[0].text}
    return _run_async(_call())
```

**Step 3:** Register in `src/agent/agent.py`:

```python
from .tools import search_documents, add_document, your_new_tool

document_agent = Agent(
    tools=[search_documents, add_document, your_new_tool],
)
```

### Change LLM Model

Edit `src/agent/agent.py`:

```python
document_agent = Agent(
    model=LiteLlm(model="openai/gpt-4"),  # Change model here
    # ... rest of config
)
```

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for available models.

### Configure ChromaDB

Edit `src/server.py`:

```python
def _get_chroma_client():
    import chromadb
    db_path = Path(__file__).parent.parent / "chroma_db"
    
    # Add custom configuration
    settings = chromadb.Settings(
        anonymized_telemetry=False,
        # ... more settings
    )
    
    return chromadb.PersistentClient(
        path=str(db_path),
        settings=settings
    )
```

## 🌐 Transport Modes

### STDIO (Default - Local Development)

```python
# src/server.py
if __name__ == "__main__":
    mcp.run()  # Uses STDIO
```

```python
# src/agent/tools.py
Client("src/server.py")  # Spawns subprocess
```

**Use for:** Local development, testing, single-machine deployments

### HTTP (Remote Deployment)

```python
# src/server.py
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

```python
# src/agent/tools.py  
Client("http://localhost:8000/mcp")  # HTTP connection
```

**Use for:** Production, remote servers, multiple agents, containers

## 🐛 Troubleshooting

### "Cannot connect to MCP server"

**Solution:** Make sure the server is running:
```bash
python src/server.py
```

### "Module not found"

**Solution:** Install dependencies:
```bash
uv sync
# or
pip install fastmcp chromadb google-adk nest-asyncio
```

### "Event loop is already running"

**Solution:** Already handled via `nest-asyncio` in `src/agent/tools.py`. If you still see this:
```bash
pip install nest-asyncio
```

### Path issues

The tools use relative paths. If you move files, update `src/agent/tools.py`:

```python
MCP_SERVER_PATH = os.path.join(os.path.dirname(__file__), "..", "server.py")
```

## 🚀 Production Deployment

### 1. Use HTTP Transport

Edit `src/server.py`:

```python
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",  # Accept external connections
        port=8000
    )
```

### 2. Add Authentication

```python
from fastmcp.server.auth import GoogleProvider

auth = GoogleProvider(
    client_id="your-client-id",
    client_secret="your-secret",
    base_url="https://your-domain.com"
)

mcp = FastMCP("Document Search", auth=auth)
```

### 3. Use Process Manager

```ini
# systemd service: /etc/systemd/system/mcp-server.service
[Unit]
Description=MCP Document Search Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/python-mcp
ExecStart=/usr/bin/python src/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Add Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def search_documents(query: str) -> str:
    logger.info(f"Search query: {query}")
    # ... rest of code
```

### 5. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

COPY src/ ./src/

EXPOSE 8000

CMD ["python", "src/server.py"]
```

## 🎓 Integration Examples

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "document-search": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/path/to/python-mcp"
    }
  }
}
```

### MCP Client Config

```json
{
  "command": "python",
  "args": ["src/server.py"],
  "cwd": "/path/to/mcp-template/python-mcp"
}
```

## 📚 Resources

### MCP & FastMCP
- [FastMCP Documentation](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Spec](https://modelcontextprotocol.io)

### Google ADK
- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub](https://github.com/google/adk)

### ChromaDB
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [ChromaDB GitHub](https://github.com/chroma-core/chroma)

### LiteLLM
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Supported Models](https://docs.litellm.ai/docs/providers)

## 🎯 Key Features

✅ **Clean Structure** - Organized in `src/` with clear separation of concerns  
✅ **Modular Architecture** - Agent and data layer decoupled via MCP  
✅ **Scalable** - Server can run locally or remotely  
✅ **Standardized** - Uses Model Context Protocol  
✅ **Semantic Search** - Vector-based document search with ChromaDB  
✅ **Production Ready** - STDIO and HTTP transport support  
✅ **Well Documented** - Single comprehensive README  
✅ **Type Safe** - Full type annotations  
✅ **Easy to Customize** - Clear patterns for extending functionality  

## 📄 License

This template is provided as-is for you to build upon. Customize and use it for your projects!

---

**Happy building! 🎉**

Need help? Check the [FastMCP docs](https://gofastmcp.com) or [ADK docs](https://google.github.io/adk-docs/).
