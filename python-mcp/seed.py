#!/usr/bin/env python3
"""
Seed ChromaDB with fun and interesting documents for testing.
"""

import chromadb
from pathlib import Path
import uuid

def seed_fun_documents():
    """Populate ChromaDB with a variety of fun documents."""
    
    # Initialize ChromaDB client
    db_path = Path(__file__).parent / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_path))
    
    # Create or get collection
    collection = client.get_or_create_collection(name="default")
    
    # Fun documents to add
    documents = [
        {
            "content": "The secret to happiness is not found in seeking more, but in developing the capacity to enjoy less. Ancient philosophers like the Stoics believed that true contentment comes from within, not from external circumstances. Marcus Aurelius once wrote that very little is needed to make a happy life.",
            "metadata": {"title": "Philosophy of Happiness", "category": "philosophy", "author": "Wisdom Keeper"}
        },
        {
            "content": "In the quantum realm, particles can exist in multiple states simultaneously until observed. This phenomenon, known as superposition, challenges our understanding of reality. Schrödinger's famous cat thought experiment illustrates this concept: a cat in a box could be both alive and dead until someone opens the box to observe it.",
            "metadata": {"title": "Quantum Superposition Explained", "category": "science", "difficulty": "intermediate"}
        },
        {
            "content": "The best pizza dough requires time and patience. Mix flour, water, salt, and a tiny bit of yeast. Let it ferment slowly in the fridge for 48-72 hours. This cold fermentation develops complex flavors and creates those perfect air bubbles. Stretch it gently, never use a rolling pin!",
            "metadata": {"title": "Perfect Pizza Dough Recipe", "category": "cooking", "prep_time": "72 hours"}
        },
        {
            "content": "Dragons are legendary creatures found in mythologies across the world. In Western tradition, they're often depicted as fire-breathing monsters hoarding treasure. Eastern dragons, however, are typically benevolent beings associated with wisdom, water, and good fortune. Chinese dragons don't have wings but fly through magic.",
            "metadata": {"title": "Dragons in Mythology", "category": "mythology", "cultures": "global"}
        },
        {
            "content": "The Model Context Protocol (MCP) enables AI agents to connect with external tools and data sources through a standardized interface. Think of it as USB for AI - a universal connector that lets agents access databases, APIs, search engines, and more without custom integrations for each service.",
            "metadata": {"title": "What is MCP?", "category": "technology", "type": "protocol"}
        },
        {
            "content": "Coffee beans aren't actually beans - they're seeds from coffee cherries! The two main species are Arabica (smooth, complex flavor) and Robusta (stronger, more bitter, twice the caffeine). The roasting process transforms green coffee beans through chemical reactions called the Maillard reaction, creating over 800 aromatic compounds.",
            "metadata": {"title": "Coffee Science", "category": "food-science", "fun_fact": "true"}
        },
        {
            "content": "Octopuses are incredibly intelligent invertebrates with three hearts, blue blood, and the ability to change color and texture instantly. Each of their eight arms has its own mini-brain with neurons that can make decisions independently. They can squeeze through any opening larger than their hard beak.",
            "metadata": {"title": "Amazing Octopuses", "category": "marine-biology", "intelligence": "high"}
        },
        {
            "content": "The library of Alexandria was the ancient world's greatest repository of knowledge, housing hundreds of thousands of scrolls. Its destruction (probably through multiple fires over many years rather than one dramatic event) represented an immeasurable loss to human civilization. Some estimate we lost 70% of ancient Greek literature.",
            "metadata": {"title": "Library of Alexandria", "category": "history", "time_period": "ancient"}
        },
        {
            "content": "TypeScript is a superset of JavaScript that adds static typing. It catches errors at compile time rather than runtime, making large codebases more maintainable. The TypeScript compiler (tsc) transforms TypeScript code into plain JavaScript that can run in any browser or Node.js environment.",
            "metadata": {"title": "TypeScript Overview", "category": "programming", "language": "typescript"}
        },
        {
            "content": "Lucid dreaming is the ability to become aware that you're dreaming while still in the dream, allowing you to potentially control the dream narrative. Techniques include reality checks throughout the day, keeping a dream journal, and the MILD (Mnemonic Induction of Lucid Dreams) method. Some people use it for creative problem-solving.",
            "metadata": {"title": "Lucid Dreaming Guide", "category": "psychology", "skill_level": "learnable"}
        },
        {
            "content": "Bees dance to communicate! When a forager bee finds a good source of nectar, it performs a 'waggle dance' to tell other bees the direction and distance. The angle of the dance relative to the vertical indicates the angle relative to the sun, and the duration of the waggle correlates with distance.",
            "metadata": {"title": "Bee Communication", "category": "biology", "behavior": "fascinating"}
        },
        {
            "content": "Vim is a powerful text editor with a steep learning curve but incredible efficiency once mastered. It uses modal editing: Normal mode for navigation, Insert mode for typing, Visual mode for selection, and Command mode for operations. Key philosophy: keeping your hands on the home row maximizes speed.",
            "metadata": {"title": "Vim Editor Basics", "category": "tools", "difficulty": "challenging"}
        },
        {
            "content": "The Japanese art of Kintsugi repairs broken pottery with gold or silver lacquer, highlighting the cracks rather than hiding them. This philosophy embraces the beauty of imperfection and the history of an object. The piece becomes more valuable after being broken and repaired.",
            "metadata": {"title": "Kintsugi Philosophy", "category": "art", "culture": "japanese", "meaning": "golden repair"}
        },
        {
            "content": "Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape. At the center lies a singularity where our understanding of physics breaks down. The event horizon marks the point of no return. Recent advances let us photograph black holes using planet-sized telescope arrays.",
            "metadata": {"title": "Black Holes Explained", "category": "astrophysics", "mind_blowing": "true"}
        },
        {
            "content": "Sourdough bread uses wild yeast and bacteria instead of commercial yeast. The starter is a living culture that must be fed regularly with flour and water. Each starter has a unique microbiome based on its environment. Sourdough is easier to digest and has a longer shelf life than commercial bread.",
            "metadata": {"title": "Sourdough Secrets", "category": "baking", "fermentation": "natural"}
        },
        {
            "content": "The ancient game of Go is deceptively simple with profound complexity. Played on a 19x19 grid, players place black and white stones to surround territory. Despite having only a few basic rules, Go has more possible positions than atoms in the observable universe. AI only mastered it recently with AlphaGo.",
            "metadata": {"title": "Game of Go", "category": "games", "origin": "china", "age": "3000+ years"}
        },
        {
            "content": "Synesthesia is a neurological condition where one sense triggers another. Some people see colors when they hear music, taste words, or see numbers as having specific colors. It's not a disorder but a different way of perceiving the world. Many artists and musicians have synesthesia.",
            "metadata": {"title": "Understanding Synesthesia", "category": "neuroscience", "type": "perception"}
        },
        {
            "content": "Fermentation is controlled decay that preserves food and creates amazing flavors. Kimchi, sauerkraut, kombucha, and yogurt all rely on beneficial bacteria. Fermented foods are packed with probiotics that support gut health. Humans have been fermenting foods for over 10,000 years.",
            "metadata": {"title": "Art of Fermentation", "category": "food-science", "health": "probiotic"}
        },
        {
            "content": "The Antikythera mechanism, discovered in a shipwreck, is an ancient Greek analog computer from 100 BCE that predicted astronomical positions and eclipses. Its complexity wouldn't be matched for over 1,000 years. It had at least 30 bronze gears and was housed in a wooden box.",
            "metadata": {"title": "Antikythera Mechanism", "category": "archaeology", "type": "ancient technology"}
        },
        {
            "content": "Crows are among the most intelligent animals on Earth. They use tools, solve complex puzzles, remember human faces for years, and can even hold grudges. They've been observed making hooks from wire, using cars to crack nuts, and teaching these behaviors to their offspring.",
            "metadata": {"title": "Crow Intelligence", "category": "ornithology", "intelligence": "remarkable"}
        }
    ]
    
    # Prepare data for batch insertion
    ids = [str(uuid.uuid4()) for _ in documents]
    contents = [doc["content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    
    # Add all documents to the collection
    collection.add(
        ids=ids,
        documents=contents,
        metadatas=metadatas
    )
    
    print(f"✅ Successfully seeded {len(documents)} documents into ChromaDB!")
    print(f"📍 Database location: {db_path}")
    print(f"\n📚 Documents added:")
    for doc in documents:
        print(f"  • {doc['metadata']['title']} ({doc['metadata']['category']})")
    
    print(f"\n🔍 Try searching for:")
    print("  - 'how do bees communicate'")
    print("  - 'ancient technology'")
    print("  - 'quantum physics'")
    print("  - 'perfect pizza recipe'")
    print("  - 'intelligent animals'")
    print("  - 'what is MCP protocol'")
    print("  - 'japanese art and philosophy'")


if __name__ == "__main__":
    seed_fun_documents()

