# AI Orchestrator

Central intelligence layer governing all AI interactions. Business services never call LLM providers directly.

## Responsibilities

- Model selection based on task type, cost, and availability
- Retry policy with exponential backoff
- Automatic provider failover (Azure OpenAI → Claude → Gemini)
- Token tracking per request
- Cost tracking and budget enforcement
- Prompt version routing
- Response validation against expected schema and safety policies
- Routing decisions based on latency, cost, and availability
