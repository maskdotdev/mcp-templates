import os
import chromadb


def seed_documents():
    chroma_client = chromadb.PersistentClient(
        path=os.path.join(os.path.dirname(__file__), "chroma_db")
    )
    documents_collection = chroma_client.get_or_create_collection(name="documents")
    
    sample_documents = [
        {
            "id": "sea_shanty",
            "content": """Yo ho ho and a bottle of rum!
            
            Fifteen men on a dead man's chest,
            Yo ho ho and a bottle of rum!
            Drink and the devil had done for the rest,
            Yo ho ho and a bottle of rum!
            
            We be sailin' the seven seas, me hearties!
            With the wind in our sails and treasure in sight.
            The Jolly Roger flies high above the mast,
            As we plunder and pillage through the night!
            
            Heave ho, haul together,
            Hoist the colors high!
            Thieves and beggars, never shall we die!""",
            "metadata": {"type": "sea_shanty", "language": "pirate", "category": "music"}
        },
        {
            "id": "python_guide",
            "content": """Python Programming Guide
            
            Python is a high-level, interpreted programming language known for its simplicity and readability.
            It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
            
            Key features:
            - Easy to learn and use
            - Extensive standard library
            - Large ecosystem of third-party packages
            - Dynamic typing
            - Automatic memory management
            
            Common use cases include web development, data analysis, machine learning, automation, and scripting.""",
            "metadata": {"type": "technical_guide", "topic": "programming", "language": "python"}
        },
        {
            "id": "recipe_pasta",
            "content": """Classic Spaghetti Carbonara Recipe
            
            Ingredients:
            - 400g spaghetti
            - 200g pancetta or guanciale
            - 4 large eggs
            - 100g Pecorino Romano cheese, grated
            - Black pepper
            - Salt
            
            Instructions:
            1. Cook pasta in salted boiling water until al dente
            2. While pasta cooks, fry pancetta until crispy
            3. Beat eggs with grated cheese and black pepper
            4. Drain pasta, reserving some pasta water
            5. Mix hot pasta with pancetta, then remove from heat
            6. Quickly stir in egg mixture, adding pasta water if needed
            7. Serve immediately with extra cheese and pepper""",
            "metadata": {"type": "recipe", "cuisine": "italian", "difficulty": "medium"}
        },
        {
            "id": "pirate_code",
            "content": """The Pirate Code of Conduct
            
            Arr matey! Every scallywag aboard this vessel must follow the code:
            
            1. Every man has a vote in affairs of moment and equal right to fresh provisions
            2. Every man to be called fairly in turn by list on board of prizes
            3. No person to game at cards or dice for money
            4. The lights and candles to be put out at eight o'clock at night
            5. To keep piece, cutlass, and pistols clean and fit for service
            6. No boy or woman to be allowed amongst the crew
            7. To desert the ship in battle be punished with death or marooning
            8. No striking one another aboard, every quarrel to be ended on shore
            
            He that breaks these rules shall suffer what punishment the Captain and crew see fit!
            Walk the plank, ye scurvy dog!""",
            "metadata": {"type": "rules", "language": "pirate", "category": "code_of_conduct"}
        },
        {
            "id": "chromadb_intro",
            "content": """Introduction to ChromaDB
            
            ChromaDB is an open-source embedding database designed for building AI applications.
            It provides a simple interface for storing and querying embeddings with their associated metadata.
            
            Key features:
            - Persistent and in-memory storage options
            - Semantic search using embeddings
            - Automatic embedding generation
            - Metadata filtering
            - Python and JavaScript clients
            
            ChromaDB is particularly useful for:
            - Retrieval Augmented Generation (RAG) systems
            - Semantic search applications
            - Document similarity matching
            - AI-powered recommendation systems""",
            "metadata": {"type": "technical_guide", "topic": "database", "category": "ai"}
        }
    ]
    
    for doc in sample_documents:
        try:
            documents_collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )
            print(f"✓ Added document: {doc['id']}")
        except Exception as e:
            print(f"✗ Failed to add {doc['id']}: {str(e)}")
    
    print(f"\n🎉 Successfully seeded {len(sample_documents)} documents into ChromaDB!")


if __name__ == "__main__":
    seed_documents()
