# AI Case Summarization Platform

Enterprise-grade AI solution for automated case summarization and conversational Q&A, designed for fraud prevention analysts.

## Documentation

| Document | Description |
|---|---|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Full architecture design — system flows, components, security, cost governance, observability |
| [`docs/images/`](./docs/images/) | Architecture diagrams (PNG) |

## Architecture Diagram

![AI Case Summarization Platform — End-to-End Architecture](./docs/images/final_architecture.png)

## Project Structure

```
CasePilot/
├── ARCHITECTURE.md                  # Full architecture document
├── README.md                        # This file
├── docs/
│   └── images/
│       └── final_architecture.png   # End-to-end architecture diagram
└── services/
    ├── api-gateway/                 # Request routing, auth, rate limiting
    ├── summary-consumer/            # Kafka consumer, data aggregation, summary workflow
    ├── chat-service/                # Conversation orchestrator, session mgmt, streaming
    ├── cost-service/                # Token usage tracking, cost calculation
    ├── pii-redaction/               # Privacy layer — redacts PII before LLM calls
    ├── llm-provider/                # Multi-provider abstraction (Azure OpenAI, Claude, Gemini)
    └── context-builder/             # Structured prompt construction
```

## Services

| Service | Responsibility |
|---|---|
| **API Gateway** | Authentication, authorization, routing, rate limiting |
| **Summary Consumer** | Kafka event processing, data aggregation, summary generation |
| **Chat Service** | Conversation management, session handling, response streaming |
| **Cost Service** | Token usage tracking, cost calculation, budget governance |
| **PII Redaction** | Privacy protection — masks sensitive data before LLM calls |
| **LLM Provider** | Multi-provider abstraction with failover and circuit breaker |
| **Context Builder** | Structured prompt construction from case data |

## Design Decisions

| Decision | Reason |
|---|---|
| Kafka | Reliable asynchronous processing |
| Redis | Low-latency caching |
| PostgreSQL | Strong transactional consistency |
| Azure OpenAI | Enterprise-grade AI capabilities |
| PII Redaction Layer | Compliance and privacy protection |
| API Gateway | Centralized routing and security |
| LLM Provider Layer | Vendor independence and failover |
| Cost Tracking Service | AI governance and budgeting |
