import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { DocumentSearchTool } from "./tools";

class DocumentSearchServer {
  private server: Server;
  private searchTool: DocumentSearchTool;

  constructor() {
    this.server = new Server(
      {
        name: "document-search-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      },
    );

    this.searchTool = new DocumentSearchTool();
    this.setupToolHandlers();
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "search_documents",
            description: "Search for documents using keyword similarity",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "The search query to find relevant documents",
                },
                limit: {
                  type: "number",
                  description:
                    "Maximum number of results to return (default: 5)",
                  default: 5,
                },
              },
              required: ["query"],
            },
          },
          {
            name: "get_all_documents",
            description: "Get all available documents",
            inputSchema: {
              type: "object",
              properties: {},
            },
          },
          {
            name: "get_document",
            description: "Get a specific document by ID",
            inputSchema: {
              type: "object",
              properties: {
                id: {
                  type: "string",
                  description: "The document ID to retrieve",
                },
              },
              required: ["id"],
            },
          },
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      if (name === "search_documents") {
        const { query, limit = 5 } = args as {
          query: string;
          limit?: number;
        };

        const results = this.searchTool.search(query, limit);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  query,
                  results,
                  total_results: results.length,
                },
                null,
                2,
              ),
            },
          ],
        };
      }

      if (name === "get_all_documents") {
        const documents = this.searchTool.getAllDocuments();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  documents,
                  total: documents.length,
                },
                null,
                2,
              ),
            },
          ],
        };
      }

      if (name === "get_document") {
        const { id } = args as { id: string };
        const document = this.searchTool.getDocumentById(id);

        if (!document) {
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ error: "Document not found" }),
              },
            ],
          };
        }

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(document, null, 2),
            },
          ],
        };
      }

      throw new Error(`Unknown tool: ${name}`);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Document Search MCP Server running on stdio");
  }
}

const server = new DocumentSearchServer();
server.run().catch(console.error);

