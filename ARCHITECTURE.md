# CasePilot V2
## AI-Powered Security Investigation Assistant
### High Level Design (HLD)

**Author:** Bhupender Sharma
**Version:** 2.1
**Status:** Technical Proposal
**Target Audience:** Architects, Engineering Leads, Security Teams

---

# 1. Executive Summary

CasePilot V2 is an AI-powered investigation platform designed to assist security analysts in understanding and investigating fraud, risk, and security-related cases.

The platform integrates with existing enterprise systems, automatically generates investigation summaries, and provides a conversational interface for analysts to ask questions about a case.

The solution follows a service-oriented architecture and centralizes all AI interactions through a dedicated AI Gateway Service, allowing the organization to remain provider-agnostic while maintaining security, observability, and operational control.

---

# 2. Problem Statement

Security analysts often need to review information spread across multiple systems:

- Case Management System
- Customer Management System
- Payment Platform
- Session & Device Intelligence Platform
- Risk & Fraud Detection Systems

As a result:

- Investigations are slow
- Context gathering is manual
- Summaries are inconsistent
- Knowledge is difficult to transfer
- Analysts spend more time collecting information than analyzing it

CasePilot aims to reduce investigation time by automatically aggregating information and presenting it through AI-generated summaries and conversational interfaces.

---

# 3. Goals

## Functional Goals

- Automatic case summarization
- AI-powered chat assistant
- Multi-model LLM support
- Cost tracking and monitoring
- Secure processing of customer data

## Non-Functional Goals

- Scalability
- Reliability
- Security
- Auditability
- Provider independence
- Cost optimization

---

# 4. High-Level Architecture

The system consists of three primary business capabilities:

## Summary Generation Flow
Generates AI summaries when case events occur.

## Chat & Q&A Flow
Allows analysts to interact with case data using natural language.

## Cost & Usage Tracking
Tracks AI usage, token consumption, and operational costs.

A dedicated AI Gateway Service centralizes all communication with LLM providers.

---

# 5. Architecture Principles

## Separation of Responsibilities
Each service owns a specific business capability.

## Event-Driven Processing
Case updates are processed asynchronously through Kafka.

## Provider Agnostic Design
Business services never directly call OpenAI, Claude, or Gemini. All AI interactions occur through AI Gateway.

## Security First
PII is removed before information is sent to external AI providers.

## Observability
All requests, failures, and token consumption are tracked.

---

# 6. Core Services

| Service | Responsibility |
|----------|----------------|
| Summary Service | Generates case summaries |
| Chat Service | Handles analyst conversations |
| AI Gateway Service | Manages LLM providers |
| Cost Service | Tracks usage and costs |
| Kafka | Event transport |
| Redis | Session caching |
| Summary Database | Stores summaries |
| Chat Database | Stores conversations |
| Usage Database | Stores AI metrics |

---

# 7. Summary Generation Service — Deep Dive

## 7.1 Overview

The Summary Generation Service is the primary value-delivery component of CasePilot. It consumes case lifecycle events from Kafka, aggregates investigation data from four upstream systems, applies security controls, and produces structured AI-generated investigation summaries.

This section provides the technical detail needed to implement this service.

---

## 7.2 Kafka Consumer Design

The service uses a Kafka consumer group with configurable concurrency.

**Consumer Group:** `casepilot-summary-consumer`

**Topic:** `case-events`

**Partition Strategy:** Messages are partitioned by `caseId` to guarantee ordered processing per case.

**Consumer Configuration:**

```yaml
kafka:
  bootstrap-servers: kafka-broker:9092
  consumer:
    group-id: casepilot-summary-consumer
    auto-offset-reset: earliest
    enable-auto-commit: false
    max-poll-records: 10
    max-poll-interval-ms: 300000
    session-timeout-ms: 30000
    concurrency: 3
```

**Why manual commit:** Auto-commit risks marking a message as consumed before processing completes. If the service crashes mid-processing, the message is lost. With manual commit, the offset is committed only after the summary is persisted. This guarantees at-least-once delivery.

**Input Event Schema:**

```json
{
  "eventId": "evt-a8f3c912",
  "caseId": "CASE-1001",
  "eventType": "CASE_CREATED",
  "timestamp": "2026-06-10T10:00:00Z",
  "source": "case-management-service",
  "version": "1.0"
}
```

**Supported Event Types:**
- `CASE_CREATED` — Full summary generation
- `CASE_UPDATED` — Conditional regeneration (only if material change detected)
- `CASE_REOPENED` — Full summary regeneration

**Event Validation:**

Before processing, each event is validated:

1. Schema validation (required fields: eventId, caseId, eventType, timestamp)
2. Duplicate detection using `eventId` stored in Redis (TTL 24h)
3. Event type whitelist check

Invalid or duplicate events are acknowledged without processing. Malformed events are routed to `case-events-dlq`.

---

## 7.3 Data Aggregation Strategy

The service makes parallel HTTP calls to four upstream services to collect investigation context. Parallel execution is critical because sequential calls would add 2-4 seconds of latency per additional system.

**Aggregation Flow:**

```
Kafka Event Received
       |
       v
  ┌────┴────┐
  │ Parallel │
  │  Calls   │
  └────┬────┘
       |
  ┌────┼────────┼────────┼────────┐
  v    v        v        v        v
Case  Customer Payment  Session  Rules
Svc   Svc      Svc      Svc      Engine
  |    |        |        |        |
  └────┼────────┼────────┼────────┘
       |
       v
  Aggregated Context
```

**Timeout and Fallback per Service:**

| Service | Timeout | Retry | On Failure |
|---------|---------|-------|------------|
| Case Management | 3s | 1 retry | Abort — case data is required |
| Customer System | 2s | 1 retry | Proceed with partial data, flag in summary |
| Payment System | 3s | 1 retry | Proceed with partial data, flag in summary |
| Session System | 2s | 1 retry | Proceed without session data |

**Why Case Management is mandatory:** Without case details (alerts, risk score, case status), a summary would be meaningless. Other data sources enrich the summary but are not strictly required.

**Aggregated Context Model:**

```json
{
  "caseId": "CASE-1001",
  "caseStatus": "OPEN",
  "riskScore": 82,
  "createdAt": "2026-06-10T08:30:00Z",
  "alerts": [
    {
      "alertId": "ALR-501",
      "type": "VELOCITY_CHECK",
      "severity": "HIGH",
      "description": "15 transactions in 2 hours from 3 countries",
      "triggeredAt": "2026-06-10T08:25:00Z"
    }
  ],
  "customer": {
    "customerId": "CUST-2200",
    "accountAge": "P2Y3M",
    "kycStatus": "VERIFIED",
    "riskTier": "MEDIUM"
  },
  "transactions": [
    {
      "txnId": "TXN-9001",
      "amount": 1250.00,
      "currency": "EUR",
      "merchant": "Electronics Store XY",
      "country": "DE",
      "timestamp": "2026-06-10T08:20:00Z",
      "status": "COMPLETED",
      "riskFlags": ["CROSS_BORDER", "HIGH_AMOUNT"]
    }
  ],
  "sessions": [
    {
      "sessionId": "SES-7700",
      "device": "iPhone 15 Pro",
      "ip": "REDACTED",
      "country": "NL",
      "loginAt": "2026-06-10T08:15:00Z",
      "fingerprint": "fp-abc123"
    }
  ],
  "dataCompleteness": {
    "caseData": true,
    "customerData": true,
    "paymentData": true,
    "sessionData": true
  }
}
```

The `dataCompleteness` field tells the LLM (and the analyst) which data sources were available. If `sessionData` is false, the summary will include a note: "Session data was unavailable during summary generation."

---

## 7.4 PII Redaction Pipeline

PII redaction occurs in two stages before data reaches the AI provider.

**Stage 1 — Pattern-Based Redaction (Regex)**

Fast, deterministic replacement of structured PII:

| Pattern | Example | Replacement |
|---------|---------|-------------|
| Email | john@example.com | [EMAIL_1] |
| Phone | +44 7911 123456 | [PHONE_1] |
| IBAN | DE89 3704 0044 0532 0130 00 | [IBAN_1] |
| Credit Card | 4111 1111 1111 1111 | [CARD_1] |
| IP Address | 192.168.1.100 | [IP_1] |

**Stage 2 — Named Entity Recognition (NER)**

Uses Microsoft Presidio for unstructured PII:

| Entity | Example | Replacement |
|--------|---------|-------------|
| Person Name | John Smith | [PERSON_1] |
| Address | 123 Baker Street, London | [ADDRESS_1] |
| Organization | Acme Corp | [ORG_1] |

**What is NOT redacted (and why):**

- Transaction amounts — LLM needs these for risk analysis
- Timestamps — Required for temporal pattern detection
- Risk scores — Core to investigation logic
- Alert types — Needed for summary categorization
- Country codes — Required for cross-border analysis

**Re-identification:**

After the LLM generates the summary, placeholders like `[PERSON_1]` are replaced back with the original values using an in-memory mapping. This mapping exists only for the duration of the request and is never persisted or logged.

---

## 7.5 Context Window Management

A fraud case can contain 200+ transactions. Sending all of them to the LLM would exceed the context window and waste tokens.

**Token Budget Allocation:**

```
Total context window:  128,000 tokens (GPT-4o)
System prompt:           1,500 tokens (fixed)
Case metadata:           1,000 tokens (fixed)
Customer profile:          500 tokens (fixed)
Alerts:                  1,500 tokens (~15 alerts max)
Transactions:            4,000 tokens (~40 transactions)
Sessions:                1,500 tokens (~15 sessions)
Response buffer:         4,000 tokens (for generated summary)
─────────────────────────────────────
Used:                   14,000 tokens
```

**Entity Prioritization:**

When entities exceed their budget, they are ranked by a priority score:

```
priority = 0.4 * risk_score + 0.25 * recency + 0.2 * amount_normalized + 0.15 * anomaly_count
```

Top-K entities per type are included. Remaining entities are summarized as: "Additionally, 162 transactions totaling EUR 45,230 occurred between 2026-06-01 and 2026-06-10. Full details available in the payment system."

**Large Case Strategy (200+ entities):**

For exceptionally large cases, a map-reduce approach is used:

1. Chunk entities into groups of 40
2. Generate a mini-summary for each chunk
3. Merge mini-summaries into a final summary

This costs ~3x more tokens but ensures no significant information is lost.

---

## 7.6 Prompt Engineering

The prompt sent to the LLM is structured, versioned, and stored in a Prompt Repository.

**System Prompt (v2.3):**

```
You are a fraud investigation assistant for a financial institution.

Your task is to analyze the provided case data and produce a structured
investigation summary.

RULES:
1. Base your analysis ONLY on the provided data
2. Never invent transactions, alerts, or entities that are not in the input
3. If data is missing, explicitly state what is unavailable
4. Use professional language suitable for compliance documentation
5. Include specific transaction IDs, amounts, and timestamps when referencing data
6. Provide a risk assessment with supporting evidence

OUTPUT FORMAT (JSON):
{
  "overview": "2-3 sentence case overview",
  "keyFindings": ["finding 1", "finding 2"],
  "riskAssessment": {
    "level": "HIGH|MEDIUM|LOW",
    "factors": ["factor 1", "factor 2"],
    "score": 82
  },
  "timelineOfEvents": [
    {"timestamp": "...", "event": "...", "significance": "..."}
  ],
  "entitiesInvolved": ["entity 1", "entity 2"],
  "recommendedActions": ["action 1", "action 2"],
  "dataGaps": ["gap 1"]
}
```

**Why JSON output format:** Structured JSON output allows the frontend to render each section independently (e.g., risk assessment as a color-coded badge, timeline as a visual component). It also enables programmatic validation — we can verify the response contains all required fields.

**Prompt Versioning:**

| Version | Change | Date |
|---------|--------|------|
| v1.0 | Initial prompt | 2026-05-01 |
| v2.0 | Added timeline of events | 2026-05-15 |
| v2.1 | Added data gaps section | 2026-05-20 |
| v2.3 | Refined risk assessment format | 2026-06-01 |

Every generated summary records the prompt version used, enabling comparison and rollback.

---

## 7.7 Response Validation (Anti-Hallucination)

LLMs can generate plausible but incorrect information. In fraud investigation, a hallucinated transaction could lead to a wrong decision.

**Validation Rules:**

1. **Schema validation** — Response must match expected JSON structure
2. **Entity cross-reference** — Every transaction ID mentioned in the summary must exist in the input data. If the LLM references `TXN-9999` but no such transaction was provided, it is flagged and removed.
3. **Amount verification** — If the summary states "a transaction of EUR 5,000," the actual amount is cross-checked against input data.
4. **Completeness check** — All required sections must be present
5. **Content safety** — No prompt leakage (system prompt appearing in output)

**On validation failure:**

- Minor issues (missing optional field): Auto-fix and proceed
- Entity hallucination: Remove the hallucinated reference, add a warning
- Major failure (invalid JSON, empty response): Retry with same prompt (max 2 retries)
- Persistent failure: Store a "generation failed" record, notify analyst

---

## 7.8 Persistence and Versioning

**Database Schema:**

```sql
CREATE TABLE case_summary (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         VARCHAR(100) NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    summary_json    JSONB NOT NULL,
    model_name      VARCHAR(50) NOT NULL,
    model_provider  VARCHAR(50) NOT NULL,
    prompt_version  VARCHAR(20) NOT NULL,
    input_tokens    INTEGER NOT NULL,
    output_tokens   INTEGER NOT NULL,
    cost_usd        DECIMAL(10,6) NOT NULL,
    processing_ms   INTEGER NOT NULL,
    data_completeness JSONB NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    
    CONSTRAINT uq_case_version UNIQUE (case_id, version)
);

CREATE INDEX idx_summary_case_id ON case_summary(case_id);
CREATE INDEX idx_summary_created ON case_summary(created_at);
```

**Why JSONB for summary:** The summary structure evolves as prompt versions change. JSONB allows schema flexibility without migrations. PostgreSQL JSONB supports indexing and querying individual fields.

**Versioning:** Each re-generation increments the version. Analysts can view previous versions. The latest version is served by default.

---

## 7.9 Reliability Design

**Retry Policy:**

```
Attempt 1: Immediate
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
```

After 3 failures, the event is routed to `case-summary-dlq`.

**Idempotency:**

Key: `caseId + eventId`

Before processing, the service checks Redis for the idempotency key. If present, the event is skipped. After successful processing, the key is stored with a 24-hour TTL.

This prevents duplicate summaries when Kafka delivers the same event twice (at-least-once semantics).

**Dead Letter Queue:**

Topic: `case-summary-dlq`

DLQ messages include the original event plus error details:

```json
{
  "originalEvent": { ... },
  "errorType": "DATA_AGGREGATION_TIMEOUT",
  "errorMessage": "Case Management Service did not respond within 3s",
  "failedAt": "2026-06-10T10:01:30Z",
  "retryCount": 3
}
```

Operations teams monitor the DLQ. Messages can be replayed after the root cause is resolved.

---

## 7.10 Performance Targets

| Metric | Target |
|--------|--------|
| End-to-end latency (P50) | < 8 seconds |
| End-to-end latency (P95) | < 15 seconds |
| Data aggregation (P95) | < 3 seconds |
| LLM response (P95) | < 10 seconds |
| Success rate | > 99% |
| Throughput | 100 summaries/minute |

---

# 8. AI Gateway Service — Deep Dive

## 8.1 Overview

The AI Gateway is the single point of contact between CasePilot business services and external LLM providers. It encapsulates all AI-specific concerns: provider routing, retry logic, circuit breaking, failover, token tracking, cost calculation, and response validation.

No business service (Summary, Chat, or any future service) communicates directly with an LLM provider.

---

## 8.2 API Contract

### Generate Summary

```http
POST /api/v1/ai/generate

Content-Type: application/json
Authorization: Bearer <service-token>
X-Correlation-Id: corr-abc123
X-Idempotency-Key: CASE-1001:v2.3:evt-a8f3c912

{
  "requestType": "SUMMARY",
  "caseId": "CASE-1001",
  "context": { ... },
  "promptVersion": "v2.3",
  "maxTokens": 4000,
  "temperature": 0.2,
  "responseFormat": "json",
  "priority": "NORMAL",
  "callerService": "summary-service"
}
```

### Response

```json
{
  "requestId": "req-xyz789",
  "status": "SUCCESS",
  "provider": "azure-openai",
  "model": "gpt-4o",
  "response": { ... },
  "usage": {
    "inputTokens": 3200,
    "outputTokens": 1850,
    "totalTokens": 5050,
    "costUsd": 0.065
  },
  "latencyMs": 4200,
  "promptVersion": "v2.3",
  "timestamp": "2026-06-10T10:00:05Z"
}
```

### Generate Chat Response

```http
POST /api/v1/ai/chat

{
  "requestType": "CHAT",
  "caseId": "CASE-1001",
  "conversationId": "conv-456",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Why was this customer flagged?"}
  ],
  "maxTokens": 2000,
  "temperature": 0.3,
  "stream": true,
  "callerService": "chat-service"
}
```

---

## 8.3 Request Processing Pipeline

Every request passes through a 7-stage pipeline:

```
Request Received
      |
      v
[1] Request Validation
      |
      v
[2] Rate Limit Check
      |
      v
[3] Provider Selection
      |
      v
[4] Prompt Assembly
      |
      v
[5] LLM Execution (with retry + failover)
      |
      v
[6] Response Validation
      |
      v
[7] Usage Recording + Response Return
```

### Stage 1: Request Validation

Validates:
- Required fields present
- `maxTokens` within allowed range (100-8000)
- `temperature` within range (0.0-1.0)
- `requestType` is known
- Payload size < 500KB
- `callerService` is registered

Rejected requests return HTTP 400 with specific error codes.

### Stage 2: Rate Limit Check

Rate limits are enforced per caller service using Redis:

```
Key:    ratelimit:{callerService}:{minute}
Value:  request count
TTL:    60 seconds
```

| Caller | Limit |
|--------|-------|
| summary-service | 200 requests/minute |
| chat-service | 500 requests/minute |

When the limit is exceeded, HTTP 429 is returned with a `Retry-After` header.

### Stage 3: Provider Selection

The Provider Router selects the LLM provider based on a routing policy:

```yaml
routing:
  default-provider: azure-openai
  rules:
    - request-type: SUMMARY
      model: gpt-4o-mini
      provider: azure-openai
      reason: "Structured extraction; mini handles it well at 10x lower cost"
    
    - request-type: CHAT
      model: gpt-4o
      provider: azure-openai
      reason: "Complex reasoning requires stronger model"
    
    - request-type: CHAT
      condition: context_tokens > 100000
      model: claude-3.5-sonnet
      provider: anthropic
      reason: "Claude has 200K context window for very large cases"
  
  failover-chain:
    - azure-openai
    - anthropic
    - google-gemini
```

**Why GPT-4o-mini for summaries:** Summarization is structured extraction from provided data. Mini handles this well and costs ~10x less ($0.15 vs $2.50 per 1M input tokens). The cost difference at 1,000 cases/day is significant: ~$0.70/day vs ~$7.00/day.

**Why GPT-4o for chat:** Analyst questions require reasoning about complex fraud patterns ("Why might these transactions be related?"). GPT-4o's stronger reasoning capability justifies the premium.

### Stage 4: Prompt Assembly

The gateway loads the prompt template from the Prompt Repository, injects the context data, and counts tokens before sending.

**Token counting** uses tiktoken (for OpenAI models) or provider-specific tokenizers. If the assembled prompt exceeds 80% of the model's context window, the Context Builder is asked to reduce the context.

### Stage 5: LLM Execution with Retry and Failover

This is the most complex stage.

**Retry Policy:**

```
Attempt 1: Primary provider (e.g., Azure OpenAI)
  |
  ├── Success → proceed to Stage 6
  |
  ├── 429 (Rate Limited) → wait Retry-After header, retry same provider
  |
  ├── 500/502/503 → wait 1s, retry same provider
  |
  └── Timeout (30s) → failover to next provider
  
Attempt 2: Same or next provider (based on error type)
  |
  ├── Success → proceed to Stage 6
  |
  └── Failure → failover to next provider

Attempt 3: Next provider in failover chain
  |
  ├── Success → proceed to Stage 6
  |
  └── Failure → return error to caller
```

**Circuit Breaker:**

Each provider has an independent circuit breaker:

```yaml
circuit-breaker:
  azure-openai:
    failure-threshold: 5          # consecutive failures to open
    success-threshold: 3          # successes to close from half-open
    timeout-duration: 30s         # time in open state before half-open
    
  anthropic:
    failure-threshold: 5
    success-threshold: 3
    timeout-duration: 30s
```

**Circuit Breaker States:**

```
CLOSED (normal operation)
  |
  5 consecutive failures
  |
  v
OPEN (all requests fail fast, no calls to provider)
  |
  30 seconds elapsed
  |
  v
HALF-OPEN (allow 1 test request)
  |
  ├── Success → back to CLOSED
  └── Failure → back to OPEN
```

When a circuit is OPEN, the Provider Router automatically skips that provider and routes to the next one in the failover chain. The caller is unaware of the failover.

**Failover Decision Table:**

| Error | Action |
|-------|--------|
| HTTP 429 (Rate Limit) | Respect Retry-After, then retry same provider |
| HTTP 500/502/503 | Retry same provider once, then failover |
| Timeout (>30s) | Immediate failover to next provider |
| HTTP 401/403 | Do NOT retry. Alert operations. Return error. |
| Network error | Failover to next provider |
| Circuit OPEN | Skip provider, use next in chain |

### Stage 6: Response Validation

After receiving the LLM response:

1. **Format check** — If JSON was requested, verify parseable JSON
2. **Completeness** — All required fields present
3. **Safety** — No system prompt leakage detected
4. **Token count** — Verify reported usage matches expectations (alert on 50%+ deviation)

### Stage 7: Usage Recording

Every request is recorded asynchronously (fire-and-forget to Kafka):

```json
{
  "requestId": "req-xyz789",
  "callerService": "summary-service",
  "caseId": "CASE-1001",
  "requestType": "SUMMARY",
  "provider": "azure-openai",
  "model": "gpt-4o-mini",
  "promptVersion": "v2.3",
  "inputTokens": 3200,
  "outputTokens": 1850,
  "costUsd": 0.065,
  "latencyMs": 4200,
  "status": "SUCCESS",
  "retryCount": 0,
  "failoverOccurred": false,
  "timestamp": "2026-06-10T10:00:05Z",
  "correlationId": "corr-abc123"
}
```

This event is consumed by the Cost Service for dashboards, budget alerts, and trend analysis.

---

## 8.4 Cost Calculation Engine

Token costs are calculated using a versioned pricing table:

```yaml
pricing:
  version: "2026-06"
  models:
    gpt-4o-mini:
      input-per-1m: 0.15
      output-per-1m: 0.60
    gpt-4o:
      input-per-1m: 2.50
      output-per-1m: 10.00
    claude-3.5-sonnet:
      input-per-1m: 3.00
      output-per-1m: 15.00
    gemini-1.5-pro:
      input-per-1m: 1.25
      output-per-1m: 5.00
```

**Cost Formula:**

```
cost = (input_tokens / 1,000,000 * input_rate) + (output_tokens / 1,000,000 * output_rate)
```

**Budget Controls:**

| Control | Threshold | Action |
|---------|-----------|--------|
| Per-case cap | $0.50 | Switch to cheapest model, warn analyst |
| Per-analyst daily | 50 chat questions | Soft limit with override option |
| Global daily | $500 | Alert engineering team |

**Projected Monthly Cost (1,000 cases/day):**

| Operation | Model | Volume/Day | Daily Cost | Monthly Cost |
|-----------|-------|------------|------------|--------------|
| Summaries | GPT-4o-mini | 1,200 | $0.70 | $21 |
| Chat Q&A | GPT-4o | 3,000 | $31.00 | $930 |
| **Total** | | **4,200** | **$31.70** | **$951** |

---

## 8.5 Provider Configuration

Each provider is configured independently:

```yaml
providers:
  azure-openai:
    endpoint: https://{resource}.openai.azure.com/
    api-version: "2024-06-01"
    deployment-map:
      gpt-4o: "gpt-4o-deployment"
      gpt-4o-mini: "gpt-4o-mini-deployment"
    timeout: 30s
    max-retries: 2
    region: "westeurope"
    
  anthropic:
    endpoint: https://api.anthropic.com/v1
    timeout: 45s
    max-retries: 1
    
  google-gemini:
    endpoint: https://generativelanguage.googleapis.com/v1
    timeout: 30s
    max-retries: 1
```

**All API keys are stored in Azure Key Vault.** The gateway loads them at startup and refreshes every 12 hours.

---

## 8.6 Observability

**Metrics exposed (Prometheus):**

| Metric | Type | Labels |
|--------|------|--------|
| `ai_gateway_requests_total` | Counter | provider, model, status, caller |
| `ai_gateway_latency_seconds` | Histogram | provider, model |
| `ai_gateway_tokens_total` | Counter | provider, model, direction (input/output) |
| `ai_gateway_cost_usd_total` | Counter | provider, model |
| `ai_gateway_circuit_state` | Gauge | provider (0=closed, 1=open, 2=half-open) |
| `ai_gateway_failover_total` | Counter | from_provider, to_provider |
| `ai_gateway_retry_total` | Counter | provider, reason |

**Alerts:**

| Alert | Condition | Severity |
|-------|-----------|----------|
| High error rate | > 5% errors in 5 minutes | P2 |
| Circuit open | Any provider circuit opens | P2 |
| Cost spike | Daily cost > 2x average | P3 |
| Latency degradation | P95 > 20 seconds | P3 |
| All providers down | All circuits open | P1 |

---

# 9. Chat Service

## Overview

The Chat Service allows analysts to ask questions about a case using natural language. The service leverages previously generated summaries and conversation history.

## Responsibilities

- Receive analyst questions
- Manage conversations
- Build context
- Invoke AI Gateway
- Store history
- Return responses

## Request Flow

1. Receive analyst request
2. Load conversation history from Redis
3. Load latest case summary from Summary DB
4. Build conversational context
5. Apply PII redaction
6. Call AI Gateway
7. Store response in Chat DB
8. Stream response to analyst via SSE

## Redis Session Cache

```
Key:   chat:{caseId}:{userId}
TTL:   24 Hours
Value: Last 10 conversation turns (to bound token usage)
```

---

# 10. Security Design

## Authentication
Microsoft Entra ID

## Authorization
Role-Based Access Control (RBAC)

## PII Protection
Two-stage redaction (regex + NER) before any data reaches an LLM provider.

## Audit Logging
All AI requests are logged with: User, Timestamp, Model, Provider, Token Count, Cost, Correlation ID.

---

# 11. Monitoring & Observability

## Summary Service
- Processing latency (P50, P95)
- Success rate
- Failure rate
- DLQ depth

## AI Gateway
- Provider usage distribution
- Token consumption by model
- Cost per request
- Retry and failover counts
- Circuit breaker state

## Chat Service
- Active sessions
- Response times
- User activity

---

# 12. Future Enhancements

- Retrieval Augmented Generation (RAG) with vector search
- Prompt versioning UI with A/B testing
- Human feedback loop for summary quality
- Multi-region deployment
- Streaming responses for summary generation

---

# 13. Conclusion

CasePilot V2 provides a scalable and secure AI-assisted investigation platform.

The Summary Generation Service automates investigation summaries by aggregating information across enterprise systems, applying PII redaction, managing context windows, and validating LLM outputs against hallucination.

The AI Gateway Service centralizes all AI interactions, providing provider independence through a 7-stage request pipeline, circuit breaker failover, cost tracking, and comprehensive observability.

Together, these services establish a foundation for enterprise-grade AI adoption within security and fraud investigation workflows.
