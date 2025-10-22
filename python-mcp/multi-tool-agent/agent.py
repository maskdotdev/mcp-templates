from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import add_document, search_documents


# We use the LiteLlm model here, but you can use any model supported by AI Factory as long
# as we pass openai/{model_name}.
# See https://google.github.io/adk-docs/agents/models/#using-cloud-proprietary-models-via-litellm
root_agent = Agent(
    name="document_agent",
    model=LiteLlm(model="openai/qwen/qwen3-4b-2507"),
    description=("Agent to answer questions about documents."),
    instruction=(
        "You are a helpful agent who can search for documents. When asked about a document"
        "use the search_documents tool to check if it exists in the database."
    ),
    tools=[search_documents, add_document],
)
