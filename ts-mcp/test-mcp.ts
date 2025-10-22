import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function testMCPServer() {
  console.log("🧪 Testing MCP Server...\n");

  const transport = new StdioClientTransport({
    command: "bun",
    args: ["run", "index.ts"],
  });

  const client = new Client(
    {
      name: "test-client",
      version: "1.0.0",
    },
    {
      capabilities: {},
    }
  );

  await client.connect(transport);
  console.log("✅ Connected to MCP server\n");

  console.log("📋 Listing available tools...");
  const tools = await client.listTools();
  console.log(`Found ${tools.tools.length} tools:`);
  tools.tools.forEach((tool) => {
    console.log(`  - ${tool.name}: ${tool.description}`);
  });
  console.log();

  console.log("🔍 Testing search_documents with 'machine learning'...");
  const searchResult = await client.callTool({
    name: "search_documents",
    arguments: {
      query: "machine learning",
      limit: 2,
    },
  });
  console.log("Result:", (searchResult.content[0] as any).text);
  console.log();

  console.log("🔍 Testing search_documents with 'sea shanty'...");
  const pirateResult = await client.callTool({
    name: "search_documents",
    arguments: {
      query: "sea shanty wellerman",
      limit: 2,
    },
  });
  console.log("Result:", (pirateResult.content[0] as any).text);
  console.log();

  console.log("📚 Testing get_all_documents...");
  const allDocs = await client.callTool({
    name: "get_all_documents",
    arguments: {},
  });
  console.log("Result:", (allDocs.content[0] as any).text);
  console.log();

  console.log("📄 Testing get_document with id 'doc5'...");
  const doc = await client.callTool({
    name: "get_document",
    arguments: {
      id: "doc5",
    },
  });
  console.log("Result:", (doc.content[0] as any).text);
  console.log();

  await client.close();
  console.log("✅ All tests completed!");
  process.exit(0);
}

testMCPServer().catch((error) => {
  console.error("❌ Test failed:", error);
  process.exit(1);
});
