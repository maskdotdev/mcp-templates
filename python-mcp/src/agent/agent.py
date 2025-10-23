"""
ADK Agent that uses MCP server for document search operations.
"""
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import add_document, search_documents, list_collections


# We use the LiteLlm model here, but you can use any model supported by AI Factory
# See https://google.github.io/adk-docs/agents/models/#using-cloud-proprietary-models-via-litellm
document_agent = Agent(
    name="document_agent",
    model=LiteLlm(model="openai/qwen/qwen3-4b-2507"),
    description="Agent to answer questions about documents using MCP server.",
    instruction=(
        "You are a helpful agent who can search for documents using an MCP server. "
        "When asked about a document, use the search_documents tool to check if it exists. "
        "You can also add documents using add_document and list available collections "
        "with list_collections."
    ),
    tools=[search_documents, add_document, list_collections],
)

