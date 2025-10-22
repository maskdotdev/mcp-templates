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

A Python-based MCP implementation with multi-tool agent capabilities:

- **Multi-Tool Agent**: Extensible agent framework
- **Google ADK Integration**: Built on Google's Agent Development Kit
- **ChromaDB Support**: Vector database for semantic search
- **Web & API Interfaces**: Both web UI and REST API
- **Modern Python**: Uses UV for dependency management

**Quick Start:**
```bash
cd python-mcp
uv sync
uv run seed
adk web  # Web interface
# or
adk server  # API server
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
  "command": "uv",
  "args": ["run", "python", "-m", "multi-tool-agent"],
  "cwd": "/path/to/python-mcp"
}
```

## Features Comparison

| Feature | TypeScript | Python |
|---------|------------|--------|
| Runtime | Bun | Python 3.10+ |
| Dependencies | Minimal | Google ADK + ChromaDB |
| Setup Complexity | Simple | Moderate |
| Vector Search | No | Yes (ChromaDB) |
| Web Interface | No | Yes |
| HTTP API | Yes | Yes |
| Tool Framework | Custom | Google ADK |

## Contributing

Feel free to submit issues and pull requests to improve these templates.

## License

MIT License - see individual template directories for specific license information.