import type { SearchResult } from "./tools";

export interface AgentConfig {
  baseURL: string;
  apiKey: string;
  model: string;
}

export interface AgentResponse {
  text: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export class Agent {
  private config: AgentConfig;

  constructor(config: AgentConfig) {
    this.config = config;
  }

  async chat(message: string, context?: SearchResult[]): Promise<AgentResponse> {
    const contextText = context && context.length > 0 
      ? `Relevant documents:\n${context.map(doc => 
          `- ${doc.metadata?.title}: ${doc.content}`
        ).join('\n')}`
      : '';

    const response = await fetch(`${this.config.baseURL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: this.config.model,
        messages: [
          { 
            role: "system", 
            content: "You are a helpful assistant. Use the provided document context to answer questions accurately." 
          },
          { 
            role: "user", 
            content: contextText ? `${message}\n\n${contextText}` : message 
          }
        ],
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API error: ${response.status} - ${error}`);
    }

    const data = await response.json() as any;
    return {
      text: data.choices[0].message.content,
      usage: {
        promptTokens: data.usage?.prompt_tokens || 0,
        completionTokens: data.usage?.completion_tokens || 0,
        totalTokens: data.usage?.total_tokens || 0,
      }
    };
  }
}
