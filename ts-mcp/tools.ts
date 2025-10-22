export interface Document {
  id: string;
  content: string;
  metadata: {
    title: string;
    category: string;
  };
}

export interface SearchResult extends Document {
  similarity: number;
}

export class DocumentSearchTool {
  private documents: Document[] = [
    {
      id: "doc1",
      content:
        "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
      metadata: { title: "Machine Learning Basics", category: "AI" },
    },
    {
      id: "doc2",
      content:
        "React is a JavaScript library for building user interfaces, particularly web applications. It uses a component-based architecture.",
      metadata: { title: "React Introduction", category: "Web Development" },
    },
    {
      id: "doc3",
      content:
        "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently. They are crucial for AI applications.",
      metadata: { title: "Vector Databases", category: "Database" },
    },
    {
      id: "doc4",
      content:
        "TypeScript is a strongly typed programming language that builds on JavaScript, giving you better tooling at any scale.",
      metadata: { title: "TypeScript Overview", category: "Programming" },
    },
    {
      id: "doc5",
      content:
        "Oh, the Wellerman came to bring us sugar and tea and rum. One day, when the tonguin' is done, we'll take our leave and go. There once was a ship that put to sea, the name of the ship was the Billy of Tea. The winds blew up, her bow dipped down, oh blow, my bully boys, blow.",
      metadata: { title: "The Wellerman Sea Shanty", category: "Maritime" },
    },
  ];

  private calculateSimilarity(query: string, text: string): number {
    const queryWords = query.toLowerCase().split(/\s+/);
    const textWords = text.toLowerCase().split(/\s+/);

    let matches = 0;
    for (const qWord of queryWords) {
      for (const tWord of textWords) {
        if (tWord.includes(qWord) || qWord.includes(tWord)) {
          matches++;
          break;
        }
      }
    }

    return matches / queryWords.length;
  }

  search(query: string, limit: number = 5): SearchResult[] {
    return this.documents
      .map((doc) => ({
        ...doc,
        similarity: this.calculateSimilarity(
          query,
          doc.content + " " + doc.metadata.title,
        ),
      }))
      .filter((doc) => doc.similarity > 0)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
  }

  getAllDocuments(): Document[] {
    return [...this.documents];
  }

  addDocument(doc: Document): void {
    this.documents.push(doc);
  }

  getDocumentById(id: string): Document | undefined {
    return this.documents.find((doc) => doc.id === id);
  }
}
