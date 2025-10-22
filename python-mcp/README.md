# Python MCP Template

## Setup

Install dependencies using UV (recommended) or pip:

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

## Getting Started

Seed the project:

```bash
uv run seed
```

## Running the Agent

### Web Interface

```bash
adk web
```

### API Server

```bash
adk server
```

Create a session:

```bash
curl -X POST http://localhost:8000/apps/multi-tool-agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key1": "value1", "key2": 42}}'
```

Send a query:

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "multi-tool-agent",
    "user_id": "u_123",
    "session_id": "s_123",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Any pirate songs?"
      }]
    }
  }' | jq .
```
