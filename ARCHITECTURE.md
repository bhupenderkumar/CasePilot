# CasePilot V2

## Enterprise AI Copilot for Case Investigation & Resolution

**Author:** Bhupender Kumar
**Date:** June 2026

---

## Executive Summary

CasePilot V2 is an enterprise-grade AI platform designed to assist analysts in investigating, understanding, and resolving customer cases through automated case summarization and conversational AI capabilities.

The platform combines event-driven architecture, AI orchestration, provider abstraction, security controls, operational governance, and cost visibility to create a resilient and scalable AI solution suitable for highly regulated and security-sensitive environments.

Unlike traditional AI integrations that directly invoke Large Language Models (LLMs), CasePilot V2 introduces an AI Orchestrator layer that manages provider routing, retries, failover, prompt governance, response validation, and cost tracking. This approach allows the platform to operate reliably in production environments while maintaining flexibility to adopt new AI providers in the future.

The solution is designed with the following goals:

- Reduce analyst investigation time
- Improve consistency of case understanding
- Enable conversational access to case information
- Protect sensitive customer information
- Maintain full auditability of AI interactions
- Control and monitor AI costs
- Provide resilience against provider failures and rate limits

---

## End-to-End Architecture

![CasePilot V2 — End-to-End Architecture](docs/images/final_architecture.png)

---

## Business Problem

Security analysts frequently need to review large volumes of information distributed across multiple systems before they can understand a customer case.

This process often involves:

- Accessing multiple internal applications
- Reviewing customer information
- Analyzing payment activities
- Reviewing session data
- Correlating historical information
- Manually producing investigation summaries

The result is increased investigation time, inconsistent analyst experiences, and reduced operational efficiency.

CasePilot V2 addresses this challenge by automatically generating case summaries and providing conversational access to relevant case information through a secure AI-powered platform.

---

## Design Principles

The architecture is based on several core principles.

### Security First

Security is implemented as a foundational concern rather than an afterthought.

The platform includes:

- PII Redaction
- Prompt Injection Detection
- Prompt Guardrails
- Role-Based Access Control
- Audit Logging
- Secrets Management

Sensitive information is protected before being sent to any AI provider.

---

### Provider Agnostic Design

Business services never communicate directly with an individual AI provider.

Instead, all AI requests are routed through the LLM Provider Layer.

Benefits include:

- Vendor independence
- Easier provider migration
- Multi-provider support
- Failover capabilities
- Cost optimization opportunities

---

### Reliability by Design

The platform assumes that failures will occur.

Examples include:

- AI provider outages
- Rate limiting
- Network failures
- Timeout conditions

To address these scenarios the platform introduces:

- Retry Queues
- Dead Letter Queues (DLQ)
- Circuit Breakers
- Provider Failover
- Idempotency Controls

---

### Auditability

Every AI interaction is traceable.

The platform captures:

- User identifiers
- Case identifiers
- Prompt versions
- Model information
- Token consumption
- Response status
- Processing timestamps

This provides transparency and supports compliance requirements.

---

### Cost Awareness

AI workloads can become expensive when unmanaged.

CasePilot V2 introduces dedicated cost tracking capabilities that provide visibility into:

- Token usage
- Provider consumption
- Cost per request
- Service-level AI spend

---

## High-Level Architecture

The platform consists of three primary business flows:

1. Summary Generation (Asynchronous)
2. Chat & Q&A (Real-Time)
3. Cost & Usage Tracking

These flows are supported by a common set of platform services including authentication, governance, monitoring, auditing, and AI orchestration.

---

## Summary Generation Flow

Summary Generation is an asynchronous workflow responsible for producing case summaries when new cases are created or updated.

The process begins when an event is published to Kafka.

A summary request is placed onto the Summary Request Queue where it can be processed independently from the originating system.

This decouples summary generation from transactional business workflows and allows the platform to scale independently.

The Summary Worker Pool consumes requests from the queue and begins processing.

The worker retrieves relevant information from multiple sources including:

- Case Management Systems
- Customer Information Systems
- Payment Systems
- Session Data Sources

This information is aggregated into a unified representation of the case.

Before any AI processing occurs, the data passes through a security pipeline.

The security pipeline includes:

- PII Redaction
- Prompt Injection Detection
- Prompt Guardrails

After validation, the Context Builder transforms the aggregated information into a structured context suitable for AI processing.

The request is then forwarded to the AI Orchestrator.

The AI Orchestrator determines:

- Which model should be used
- Which provider should receive the request
- Whether retry policies apply
- Which prompt template version should be used

The request is then routed through the LLM Provider Layer.

After summary generation, results are published to the Summary Result Queue.

A Summary Persistence Service consumes the result and stores it in the Summary Database.

If processing fails, requests may be routed to:

- Retry Queue
- Dead Letter Queue

This ensures that failures can be investigated without losing data.

---

## Chat & Q&A Flow

The Chat & Q&A flow provides analysts with real-time conversational access to case information.

An analyst submits a question through the user interface.

The request is routed through the API Gateway and reaches the Chat Service.

The Chat Service retrieves conversational context from Redis Session Cache.

The request then passes through the same security pipeline used by summary generation:

- PII Redaction
- Prompt Injection Detection
- Prompt Guardrails

The Context Builder enriches the request with relevant information.

The request is then forwarded to the AI Orchestrator.

The AI Orchestrator performs:

- Model Selection
- Provider Routing
- Retry Management
- Token Tracking
- Cost Calculation
- Prompt Version Selection

The request is then processed through the LLM Provider Layer.

Generated responses undergo Response Validation before being returned to the user.

Responses are streamed back using Server-Sent Events (SSE) or WebSockets, providing a responsive user experience.

Conversations are persisted within the Chat Database for future reference and auditing.

In failure scenarios, requests may be routed through a dedicated Chat Retry Queue before ultimately reaching a Chat Dead Letter Queue if processing remains unsuccessful.

---

## AI Orchestrator

The AI Orchestrator is the central intelligence layer of the platform.

Rather than allowing business services to directly communicate with AI providers, all requests pass through this component.

Responsibilities include:

- Model Routing
- Provider Selection
- Retry Logic
- Failover Handling
- Prompt Versioning
- Cost Tracking
- Token Tracking
- Response Validation
- Policy Enforcement

This abstraction simplifies business services and centralizes AI-specific logic.

The orchestrator enables future expansion without requiring modifications across the platform.

---

## LLM Provider Layer

The LLM Provider Layer abstracts the underlying AI vendors from business services.

Supported providers may include:

- Azure OpenAI
- Anthropic Claude
- Google Gemini

Future providers can be integrated without changing upstream services.

The provider layer also supports failover scenarios.

For example:

If Azure OpenAI returns a rate-limit response, the orchestrator may retry the request or route it to an alternative provider.

This improves availability while reducing dependency on a single vendor.

---

## Prompt Management

Prompt engineering is treated as a managed asset.

CasePilot V2 introduces a Prompt Service and Prompt Repository.

Prompt templates are versioned and stored centrally.

Benefits include:

- Version Control
- Rollback Support
- A/B Testing
- Governance
- Auditability

Prompt versions are recorded alongside generated outputs, enabling complete traceability.

---

## Data Storage Strategy

The platform follows the principle of service ownership.

Each service owns its own database.

Examples include:

- Chat Database
- Summary Database
- Audit Database
- Cost Database
- Prompt Database

Benefits include:

- Independent scaling
- Reduced coupling
- Clear ownership boundaries
- Improved maintainability

---

## Caching Strategy

Redis is used as a distributed caching layer.

The platform maintains several logical cache domains.

### Session Cache

Stores active conversation state.

### Context Cache

Stores generated context payloads.

### Summary Cache

Stores frequently requested summaries.

### Response Cache

Prevents unnecessary repeated AI calls.

### Rate Limit Cache

Supports rate limiting and request throttling.

Caching improves performance while reducing AI costs.

---

## Security Architecture

Security is critical because the platform processes potentially sensitive customer information.

Key controls include:

### Microsoft Entra ID

Provides authentication and identity management.

### Role-Based Access Control

Ensures users access only authorized functionality.

### PII Redaction

Removes sensitive information before AI processing.

### Prompt Injection Detection

Identifies attempts to manipulate AI behavior.

### Prompt Guardrails

Validates prompt content and enforces policy requirements.

### Secrets Management

Credentials are stored securely using Key Vault solutions.

### Audit Logging

Captures all significant platform activity.

These controls reduce risk while supporting regulatory compliance.

---

## Audit Service

Every AI interaction is logged through a dedicated Audit Service.

Recorded information includes:

- User Identifier
- Case Identifier
- Prompt Version
- Provider
- Model
- Token Usage
- Request Status
- Cost Information
- Timestamp
- Correlation Identifier

This creates a complete audit trail.

For security-focused organizations, this capability is essential.

---

## Cost & Usage Tracking

AI platforms require operational cost visibility.

CasePilot V2 introduces a dedicated Cost & Usage Tracking workflow.

Usage events are generated by:

- AI Orchestrator
- Summary Service
- Chat Service

These events are published to Kafka.

A Cost & Usage Processor consumes these events and stores results within a dedicated Cost Database.

The platform provides:

- Cost Dashboards
- Usage Reports
- Budget Alerts
- Trend Analysis

This allows stakeholders to understand AI consumption patterns and identify optimization opportunities.

---

## Reliability & Resilience

The platform is designed to tolerate failures.

Reliability mechanisms include:

### Retry Queues

Temporary failures are retried automatically.

### Dead Letter Queues

Failed requests are isolated for investigation.

### Circuit Breakers

Prevent cascading failures.

### Provider Failover

Alternative providers can be selected when required.

### Idempotency Controls

Duplicate requests are prevented through unique processing identifiers.

### Health Monitoring

Continuous monitoring supports early issue detection.

These capabilities improve overall system stability.

---

## Monitoring & Observability

The platform includes comprehensive observability.

Key capabilities include:

- Centralized Logging
- Metrics Collection
- Distributed Tracing
- Alerting
- Operational Dashboards

The monitoring stack enables rapid diagnosis of issues and supports proactive system management.

---

## Future Roadmap

Potential future enhancements include:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Embedding Services
- Semantic Search
- Human Feedback Loops
- Multi-Agent Workflows
- Automated Model Selection
- Advanced AI Evaluation Frameworks

The current architecture has been designed to accommodate these capabilities without major structural changes.

---

## Conclusion

CasePilot V2 provides a secure, scalable, and resilient architecture for enterprise AI adoption.

By combining event-driven processing, AI orchestration, security controls, auditability, provider abstraction, and cost governance, the platform enables analysts to investigate cases more efficiently while maintaining operational control and compliance.

The architecture deliberately separates business concerns from AI concerns through the introduction of the AI Orchestrator and LLM Provider Layer. This approach allows the platform to evolve alongside rapidly changing AI technologies while preserving maintainability, reliability, and governance.

CasePilot V2 is not simply an AI integration. It is a production-ready AI platform designed to operate responsibly in security-sensitive enterprise environments.
