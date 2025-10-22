# Document Search MCP Server

A simple Model Context Protocol (MCP) server with OpenAI-compatible API integration that provides document search capabilities.

## Features

- **Keyword Search**: Simple in-memory document search using keyword matching
- **OpenAI-Compatible API**: Works with OpenAI, Ollama, LM Studio, Groq, and more
- **HTTP API**: REST endpoints for easy testing and integration
- **No External Dependencies**: No need for ChromaDB or vector databases
- **Sample Data**: Pre-loaded with sample documents about AI, web development, and programming

## Requirements

- Bun runtime
- OpenAI-compatible API endpoint (OpenAI, Ollama, LM Studio, etc.)

## Installation

```bash
bun install
```

## Setup

Configure environment variables for your AI provider:

```bash
# For LM Studio (default)
export OPENAI_BASE_URL=http://localhost:1234/v1
export OPENAI_API_KEY=lm-studio

# For Ollama
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama

# For OpenAI
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_API_KEY=sk-your-key-here

# For Groq
export OPENAI_BASE_URL=https://api.groq.com/openai/v1
export OPENAI_API_KEY=your-groq-key
```

## Usage

### Option 1: MCP Server (stdio)

Run the MCP server for use with MCP clients:

```bash
bun index.ts
```

The server runs on stdio and communicates using the MCP protocol.

### Option 2: HTTP Server (testing)

Run the HTTP server with AI SDK integration:

```bash
bun server.ts
```

Server runs on http://localhost:3000 with these endpoints:

#### `GET /health`
Health check endpoint.

#### `POST /search`
Direct document search without AI.

**Request:**
```json
{
  "query": "JavaScript library for building interfaces",
  "limit": 3
}
```

**Response:**
```json
{
  "query": "JavaScript library for building interfaces",
  "results": [
    {
      "id": "doc2",
      "content": "React is a JavaScript library...",
      "metadata": { "title": "React Introduction", "category": "Web Development" },
      "similarity": 0.85
    }
  ],
  "total": 1
}
```

#### `POST /chat`
AI-powered chat with automatic document search tool calling.

**Request:**
```json
{
  "message": "What is machine learning?",
  "model": "gpt-4o-mini"
}
```

**Response:**
```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "usage": { "promptTokens": 150, "completionTokens": 200 }
}
```

### Testing

Test the HTTP server:

```bash
bun test-server.ts
```

### Sample Documents

The server comes pre-loaded with sample documents covering:
- Machine Learning Basics
- React Introduction  
- Vector Databases
- TypeScript Overview

## MCP Client Integration

This server can be used with any MCP-compatible client. Configure your client to use:

```json
{
  "command": "bun",
  "args": ["index.ts"],
  "cwd": "/path/to/this/directory"
}
```

## Architecture

- **index.ts**: MCP server implementation (stdio transport)
- **server.ts**: HTTP server with AI SDK integration
- **ChromaDB**: Vector database for semantic search
- **AI SDK**: Vercel AI SDK for OpenAI-compatible providers
