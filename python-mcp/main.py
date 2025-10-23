#!/usr/bin/env python3
"""
ADK agent with MCP server for document management.
"""
from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm

from src.agent.tools import add_document, search_documents, list_collections, cleanup_mcp_client

APP_NAME = "document_agent"
USER_ID = "1234"
SESSION_ID = "session1234"


# Create the agent
agent = LlmAgent(
    model=LiteLlm(model="openai/qwen/qwen3-4b-2507"),
    name="document_agent",
    instruction=(
        "You are a helpful agent who can search for documents using an MCP server. "
        "When asked about a document, use the search_documents tool to check if it exists. "
        "You can also add documents using add_document and list available collections "
        "with list_collections."
    ),
    tools=[search_documents, add_document, list_collections]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)


# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")


async def main():
    """Run example queries against the document agent."""
    print("\n" + "="*70)
    print("📚 Document Agent Examples")
    print("="*70)
    
    # Example 1: List collections
    print("\n\n📋 Example 1: List available collections")
    print("-"*70)
    call_agent("What collections are available?")
    
    # Example 2: Add a document
    print("\n\n➕ Example 2: Add a new document")
    print("-"*70)
    call_agent(
        "Add a document with title 'MCP Protocol' and content "
        "'The Model Context Protocol (MCP) enables standardized communication "
        "between AI agents and external tools, allowing agents to access "
        "databases, APIs, and other resources through a unified interface.'"
    )
    
    # Example 3: Search documents
    print("\n\n🔍 Example 3: Search for documents")
    print("-"*70)
    call_agent("Search for documents about protocols or communication standards")
    
    # Example 4: Answer a question
    print("\n\n❓ Example 4: Answer a question using search")
    print("-"*70)
    call_agent("What is MCP and what does it do?")
    
    print("\n" + "="*70)
    print("✅ Examples completed!")
    print("\nTo run your own queries, use:")
    print("  call_agent('your question here')")
    
    # Cleanup
    await cleanup_mcp_client()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

