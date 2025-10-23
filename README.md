# MCP Templates

This repository contains starter templates for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers in TypeScript and Python.

## Templates

### 🔷 TypeScript Template (`ts-mcp/`)

A complete MCP server implementation with document search capabilities, featuring:

- **Document Search**: In-memory keyword search with sample documents
- **OpenAI-Compatible API**: Works with OpenAI, Ollama, LM Studio, Groq, and more
- **HTTP API**: REST endpoints for testing and integration
- **No External Dependencies**: Minimal setup, no vector databases required
- **Bun Runtime**: Fast TypeScript execution with Bun

**Quick Start:**
```bash
cd ts-mcp
bun install
bun index.ts  # MCP server (stdio)
# or
bun server.ts # HTTP server for testing
```

### 🐍 Python Template (`python-mcp/`)

A clean, production-ready template connecting Google ADK agents to MCP servers:

- **MCP Server**: FastMCP server with ChromaDB semantic search
- **ADK Agent**: Google ADK agent that consumes MCP tools
- **Semantic Search**: Vector-based document search with ChromaDB
- **Clean Structure**: Organized in `src/` with clear separation
- **Production Ready**: STDIO and HTTP transport support

**Quick Start:**
```bash
cd python-mcp
uv sync

# Terminal 1: Start MCP server
python src/server.py

# Terminal 2: Run agent example
python main.py
```

## Getting Started

1. **Choose Your Template**: Pick TypeScript or Python based on your preference
2. **Clone & Setup**: Navigate to your chosen template and follow its README
3. **Customize**: Modify the tools and capabilities for your specific use case
4. **Deploy**: Use the MCP server with your favorite MCP client

## MCP Integration

Both templates can be integrated with MCP-compatible clients. Configure your client with:

**TypeScript:**
```json
{
  "command": "bun",
  "args": ["index.ts"],
  "cwd": "/path/to/ts-mcp"
}
```

**Python:**
```json
{
  "command": "python",
  "args": ["src/server.py"],
  "cwd": "/path/to/mcp-template/python-mcp"
}
```

## Features Comparison

| Feature | TypeScript | Python |
|---------|------------|--------|
| Runtime | Bun | Python 3.10+ |
| Framework | Custom | FastMCP + Google ADK |
| Dependencies | Minimal | FastMCP + ChromaDB |
| Setup Complexity | Simple | Simple |
| Vector Search | No | Yes (ChromaDB) |
| Transport | STDIO | STDIO + HTTP |
| Agent Integration | N/A | Google ADK |
| Architecture | Direct | MCP Client-Server |

## Contributing

Feel free to submit issues and pull requests to improve these templates.

## License

MIT License - see individual template directories for specific license information.