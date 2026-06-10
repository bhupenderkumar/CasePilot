# CasePilot V2

## Enterprise AI Copilot for Case Investigation & Resolution

**Author:** Bhupender Kumar
**Date:** June 2026

---

### Core Design Principles

- **Security First** — No sensitive data leaves the platform unredacted
- **Failure Tolerant** — Retry queues, DLQs, circuit breakers, provider failover
- **Provider Agnostic** — LLM Provider Layer abstracts all AI vendors
- **Event Driven** — Kafka-based async processing for summary generation
- **Auditable** — Every AI request tracked with full traceability
- **Cost Aware** — Per-request token and cost tracking with budget controls
- **Prompt Governed** — Versioned prompts with rollback, guardrails, and injection detection
- **Horizontally Scalable** — Stateless services, worker pools, independent databases

---

## End-to-End Architecture

![CasePilot V2 — End-to-End Architecture](docs/images/final_architecture.png)

---

## System Context

```
                         ┌────────────────┐
                         │   Analysts     │
                         └───────┬────────┘
                                 │
                                 ▼

┌─────────────────────────────────────────────────────┐
│                     CASEPILOT V2                    │
│                                                     │
│ AI Copilot for Case Investigation & Resolution      │
└───────────────┬─────────────────────┬───────────────┘
                │                     │
                ▼                     ▼

      ┌─────────────────┐   ┌─────────────────┐
      │ Case Management │   │ Customer Data   │
      │ Systems         │   │ Systems         │
      └─────────────────┘   └─────────────────┘

                │
                ▼

      ┌─────────────────┐
      │ LLM Providers   │
      └─────────────────┘

        Azure OpenAI
        Claude
        Gemini
```

---

## Container Architecture

### Identity Layer

```
┌──────────────────────────────────────────────────────────┐
│                    Identity Layer                        │
├──────────────────────────────────────────────────────────┤
│ Analyst Browser                                          │
│ Microsoft Entra ID                                       │
│ API Gateway                                              │
│ RBAC                                                     │
│ Rate Limiting                                            │
└──────────────────────────────────────────────────────────┘
```

### Summary Generation Pipeline

```
Case Event
     │
     ▼
Kafka Topic
     │
     ▼
Summary Request Queue
     │
     ▼
Summary Worker Pool
     │
     ▼
Data Aggregator
     │
     ▼
PII Redaction
     │
     ▼
Prompt Injection Detection
     │
     ▼
Prompt Guardrails
     │
     ▼
Context Builder
     │
     ▼
AI Orchestrator
     │
     ▼
LLM Provider Layer
     │
     ▼
Summary Result Queue
     │
     ▼
Summary Persistence Consumer
     │
     ▼
Summary Database

     ├─────────────► Retry Queue
     │
     └─────────────► DLQ
```

### Chat Architecture

```
Analyst
    │
    ▼
Chat Service
    │
    ▼
Redis Session Cache
    │
    ▼
PII Redaction
    │
    ▼
Prompt Injection Detection
    │
    ▼
Prompt Guardrails
    │
    ▼
Context Builder
    │
    ▼
AI Orchestrator
    │
    ▼
LLM Provider Layer
    │
    ▼
Response Validation
    │
    ▼
SSE / Streaming Response
    │
    ▼
Chat Database
```

Chat failure path:

```
LLM Timeout
      │
      ▼
Chat Retry Queue
      │
      ▼
Retry Worker
      │
      ▼
LLM Provider Layer
```

---

## AI Orchestrator

The AI Orchestrator is the central intelligence layer that governs all AI interactions. Business services never call LLM providers directly — everything flows through the orchestrator.

```
┌───────────────────────────────────────────┐
│              AI ORCHESTRATOR              │
├───────────────────────────────────────────┤
│ Model Selection                           │
│ Retry Policy                              │
│ Provider Failover                         │
│ Token Tracking                            │
│ Cost Tracking                             │
│ Prompt Versioning                         │
│ Response Validation                       │
│ Routing Decisions                         │
└───────────────────────────────────────────┘
```

Responsibilities:

- **Model Selection** — Choose the right model based on task type, cost, and availability
- **Retry Policy** — Exponential backoff with configurable max attempts
- **Provider Failover** — Automatic fallback when a provider returns 429 or 5xx
- **Token Tracking** — Count input/output tokens per request for cost and budget enforcement
- **Cost Tracking** — Calculate and record per-request cost
- **Prompt Versioning** — Route to the correct prompt version for each task
- **Response Validation** — Validate LLM output against expected schema and safety policies
- **Routing Decisions** — Direct requests to the optimal provider based on latency, cost, and availability

---

## Prompt Management

```
AI Orchestrator
      │
      ▼
Prompt Service
      │
      ▼
Prompt Repository

  Version 1
  Version 2
  Version 3
```

Benefits:

- **Rollback** — Revert to a previous prompt version instantly
- **Auditability** — Track which prompt version generated which output
- **A/B Testing** — Compare prompt performance across versions

---

## LLM Provider Layer

```
┌────────────────────────────┐
│     LLM Provider Layer     │
└─────────────┬──────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼

Azure      Claude     Gemini
OpenAI
```

Failover chain:

```
Azure OpenAI
      │
      ▼
   429 / 5xx
      │
      ▼
   Claude
      │
      ▼
   Gemini
```

No business service is aware of which provider is being used. The LLM Provider Layer handles all provider-specific logic, authentication, and error handling.

---

## Caching Layer

```
Redis
  │
  ├── Session Cache       — Conversational context for Chat
  ├── Summary Cache       — Frequently accessed summaries
  ├── Response Cache      — Repeated LLM responses
  ├── Context Cache       — Pre-built context payloads
  └── Rate Limit Cache    — Per-user/per-service rate tracking
```

---

## Service-Owned Databases

Each service owns its database — no shared schemas, no cross-service queries.

```
Chat Service DB         — Conversations, sessions

Summary Service DB      — Generated summaries, versions

Audit Service DB        — AI request logs, compliance records

Cost Service DB         — Token usage, cost records, budgets

Prompt Service DB       — Prompt templates, versions, metadata
```

Benefits:

- Service isolation
- Independent scaling
- Clear data ownership
- Independent retention policies

---

## Audit Architecture

Every AI request is fully traceable.

```
Every AI Request
        │
        ▼
Audit Service
        │
        ▼
Audit Database
```

Captured fields:

```
UserId
CaseId
PromptVersion
ModelUsed
Provider
TokenCount
Cost
ResponseStatus
Timestamp
CorrelationId
```

This is particularly valuable for a security company — full auditability of every AI interaction.

---

## Reliability Layer

```
Retry Queue              — Transient failure recovery
DLQ                      — Failed message capture
Circuit Breaker          — Prevent cascading failures
Provider Failover        — Automatic LLM provider switching
Idempotency Store        — Prevent duplicate processing
Health Checks            — Continuous service monitoring
```

Idempotency key:

```
CaseId + PromptVersion
```

Prevents duplicate summaries when events are replayed or retried.

---

## Security Layer

```
Entra ID                 — Authentication
RBAC                     — Authorization
PII Redaction            — Privacy protection
Prompt Injection Detection — AI-specific threat prevention
Prompt Guardrails        — Policy enforcement
Content Filtering        — Output safety controls
Audit Logging            — Compliance tracking
Key Vault                — Secrets management
```

Defense in depth — sensitive data is redacted before it leaves the platform, prompts are validated before they reach the LLM, and outputs are filtered before they reach the analyst.

---

## Cost Governance

The platform tracks every token and every dollar.

Tracked per request:

- Model used
- Provider
- Prompt tokens
- Completion tokens
- Total cost
- Timestamp

Budget controls:

- Per-case spending cap
- Per-analyst daily limit
- Global daily budget with alerting
- Model tier switching when budget is exceeded

---

## Observability

Full monitoring and tracing across all services.

- **OpenTelemetry** — Distributed tracing
- **Azure Monitor** — Infrastructure monitoring
- **Application Insights** — Application performance
- **Prometheus** — Metrics collection
- **Grafana** — Visualization dashboards
- **Alert Manager** — Operational alerting

Every AI request carries a correlation ID from API Gateway through to the LLM provider and back.

---

## Future — V3 Roadmap

```
Vector Database          — Semantic storage
Embeddings               — Document vectorization
RAG Pipeline             — Retrieval-Augmented Generation
Knowledge Search         — Enterprise knowledge base
Multi-Agent Workflows    — Agentic AI orchestration
Feedback Learning Loop   — Human-in-the-loop improvement
```

These capabilities can be introduced with minimal impact on existing services due to the modular architecture.

---

## Summary

CasePilot V2 introduces an AI Orchestrator, provider abstraction, prompt governance, auditability, retry queues, DLQs, and provider failover to address production concerns such as rate limiting, outages, security controls, and operational governance.

The architecture is designed to support enterprise-scale AI workloads while maintaining traceability, resiliency, and future extensibility.

> The biggest change from V1: we moved from **calling an LLM** to **operating an AI platform**.
