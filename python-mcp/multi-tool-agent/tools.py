import os

import chromadb

chroma_client = chromadb.PersistentClient(
    path=os.path.join(os.path.dirname(__file__), "..", "chroma_db")
)
documents_collection = chroma_client.get_or_create_collection(name="documents")


def add_document(document_name: str, content: str) -> dict:
    """Adds a document to the ChromaDB collection.

    Args:
        document_name (str): The name/identifier of the document.
        content (str): The content of the document.

    Returns:
        dict: status and result or error msg.
    """
    try:
        documents_collection.add(
            documents=[content], metadatas=[{}], ids=[document_name]
        )
        return {
            "status": "success",
            "message": f"Document '{document_name}' added successfully.",
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to add document: {str(e)}"}


def search_documents(query: str, n_results: int = 5) -> dict:
    """Searches for documents in the ChromaDB collection based on a query.

    Args:
        query (str): The search query to find relevant documents.
        n_results (int, optional): Maximum number of results to return. Defaults to 5.

    Returns:
        dict: status with found documents, their content, and metadata, or error msg.
    """
    try:
        results = documents_collection.query(query_texts=[query], n_results=n_results)

        if not results["ids"] or not results["ids"][0]:
            return {
                "status": "success",
                "message": "No documents found matching the query.",
                "documents": [],
            }

        documents = []
        for i, doc_id in enumerate(results["ids"][0]):
            documents.append(
                {
                    "id": doc_id,
                    "content": results["documents"][0][i]
                    if results["documents"]
                    else None,
                    "metadata": results["metadatas"][0][i]
                    if results["metadatas"]
                    else {},
                    "distance": results["distances"][0][i]
                    if results["distances"]
                    else None,
                }
            )

        return {
            "status": "success",
            "message": f"Found {len(documents)} document(s).",
            "documents": documents,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search documents: {str(e)}",
        }
