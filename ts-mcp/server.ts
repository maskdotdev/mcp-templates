import { DocumentSearchTool } from "./tools";
import { Agent } from "./agent";

const searchTool = new DocumentSearchTool();
const agent = new Agent({
  baseURL: process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
  apiKey: process.env.OPENAI_API_KEY || "sk-dummy",
  model: process.env.OPENAI_MODEL || "qwen/qwen3-8b",
});

const server = Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok" }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    if (url.pathname === "/search" && req.method === "POST") {
      try {
        const body = (await req.json()) as { query?: string; limit?: number };
        const { query, limit = 5 } = body;

        if (!query) {
          return new Response(JSON.stringify({ error: "Query is required" }), {
            status: 400,
            headers: { "Content-Type": "application/json" },
          });
        }

        const results = searchTool.search(query, limit);

        return new Response(
          JSON.stringify({ query, results, total: results.length }),
          {
            headers: { "Content-Type": "application/json" },
          },
        );
      } catch (error) {
        return new Response(JSON.stringify({ error: String(error) }), {
          status: 500,
          headers: { "Content-Type": "application/json" },
        });
      }
    }

    if (url.pathname === "/chat" && req.method === "POST") {
      try {
        const body = (await req.json()) as { message?: string; model?: string };
        const { message, model = "qwen/qwen3-8b" } = body;

        if (!message) {
          return new Response(
            JSON.stringify({ error: "Message is required" }),
            {
              status: 400,
              headers: { "Content-Type": "application/json" },
            },
          );
        }

        const searchResults = searchTool.search(message, 3);
        const result = await agent.chat(message, searchResults);

        return new Response(
          JSON.stringify({
            response: result.text,
            usage: result.usage,
            documentsUsed: searchResults.length,
            documents: searchResults.map((doc) => ({
              title: doc.metadata?.title,
              similarity: doc.similarity,
            })),
          }),
          {
            headers: { "Content-Type": "application/json" },
          },
        );
      } catch (error) {
        return new Response(JSON.stringify({ error: String(error) }), {
          status: 500,
          headers: { "Content-Type": "application/json" },
        });
      }
    }

    return new Response("Not Found", { status: 404 });
  },
});

console.log(`🚀 Server running at http://localhost:${server.port}`);
console.log(`📍 Endpoints:`);
console.log(`  GET  /health - Health check`);
console.log(`  POST /search - Simple keyword-based document search`);
console.log(
  `  POST /chat   - AI chat with document search (OpenAI-compatible)`,
);
console.log(`\n⚙️  Configuration:`);
console.log(
  `  API Key: ${process.env.OPENAI_API_KEY ? "✓ Set" : "✗ Not set (using dummy key)"}`,
);
console.log(
  `  Base URL: ${process.env.OPENAI_BASE_URL || "https://api.openai.com/v1"}`,
);
console.log(`\n💡 Tip: Set OPENAI_BASE_URL to use any OpenAI-compatible API`);
console.log(`   Examples:`);
console.log(`   - Ollama:    http://localhost:11434/v1`);
console.log(`   - LM Studio: http://localhost:1234/v1`);
console.log(`   - Groq:      https://api.groq.com/openai/v1`);
