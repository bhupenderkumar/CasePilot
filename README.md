# AI Case Summarization Platform

Enterprise-grade AI solution for automated case summarization and conversational Q&A, designed for fraud prevention analysts.

## Documentation

| Document | Description |
|---|---|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Full architecture design — system flows, components, security, cost governance, observability |
| [`docs/images/`](./docs/images/) | Architecture diagrams (PNG) |

## Project Structure

```
fraud-ai-summarization/
├── ARCHITECTURE.md                  # Full architecture document
├── README.md                        # This file
├── docs/
│   ├── generate_diagrams_v2.py      # Diagram generator (diagrams 01–10)
│   ├── generate_diagram_11.py       # Diagram generator (system flow)
│   └── images/                      # Generated architecture diagrams
│       ├── 01-high-level-architecture.png
│       ├── 02-sequence-summary-generation.png
│       ├── 03-sequence-qa-flow.png
│       ├── 04-data-flow-pipeline.png
│       ├── 05-database-schema.png
│       ├── 06-resilience-architecture.png
│       ├── 07-cost-tracking.png
│       ├── 08-rollout-strategy.png
│       ├── 09-context-window.png
│       ├── 10-pii-redaction.png
│       └── 11-system-flow.png
└── services/
    ├── api-gateway/                 # Request routing, auth, rate limiting
    ├── summary-consumer/            # Kafka consumer, data aggregation, summary workflow
    ├── chat-service/                # Conversation orchestrator, session mgmt, streaming
    ├── cost-service/                # Token usage tracking, cost calculation
    ├── pii-redaction/               # Privacy layer — redacts PII before LLM calls
    ├── llm-provider/                # Multi-provider abstraction (Azure OpenAI, Claude, Gemini)
    └── context-builder/             # Structured prompt construction
```

## Architecture Diagrams

| Diagram | Description |
|---|---|
| [01 — High-Level Architecture](./docs/images/01-high-level-architecture.png) | System context with all platform components |
| [02 — Summary Generation](./docs/images/02-sequence-summary-generation.png) | Sequence: event → data collection → LLM → store |
| [03 — Q&A Flow](./docs/images/03-sequence-qa-flow.png) | Sequence: question → PII redaction → LLM → SSE streaming |
| [04 — Data Flow Pipeline](./docs/images/04-data-flow-pipeline.png) | End-to-end pipeline with failure recovery |
| [05 — Database Schema](./docs/images/05-database-schema.png) | ER diagram with tables and relationships |
| [06 — Resilience](./docs/images/06-resilience-architecture.png) | Circuit breaker + fallback chain |
| [07 — Cost Tracking](./docs/images/07-cost-tracking.png) | Token usage flow and cost projections |
| [08 — Rollout Strategy](./docs/images/08-rollout-strategy.png) | Phased rollout timeline |
| [09 — Context Window](./docs/images/09-context-window.png) | Token budgets and entity prioritization |
| [10 — PII Redaction](./docs/images/10-pii-redaction.png) | Two-stage redaction pipeline |
| [11 — System Flow](./docs/images/11-system-flow.png) | Horizontal end-to-end flow across all services |

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

## Regenerating Diagrams

```bash
pip install matplotlib
python docs/generate_diagrams_v2.py
python docs/generate_diagram_11.py
```

Output: `docs/images/*.png`
