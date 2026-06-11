CasePilot V2
High Level Design (HLD)
Author: Bhupender Sharma
Version: 2.0
Document Type: High Level Design
Date: June 2026

1. Executive Summary
Purpose
CasePilot V2 is an AI-powered investigation assistant designed to help security analysts efficiently understand, investigate, and interact with fraud and risk cases.

The platform automatically generates investigation summaries from multiple enterprise systems and provides a conversational interface that allows analysts to ask natural language questions about a case.

The solution is designed with security, scalability, observability, and provider independence in mind.

2. Business Problem
Security analysts typically need to gather information from multiple systems:

Case Management System

Customer Management System

Payment Platform

Session & Device Platform

This process is time-consuming and often results in inconsistent investigations.

Challenges
Information spread across multiple systems

Long investigation times

Manual summary creation

Inconsistent analyst experience

Lack of AI-assisted investigation capabilities

3. Goals
Functional Goals
Automated case summarization

Conversational case investigation

Multi-provider LLM support

Cost tracking and reporting

Secure handling of sensitive information

Non-Functional Goals
High availability

Scalability

Provider independence

Auditability

Security and compliance

4. High Level Architecture
(Insert Architecture Diagram Here)

The platform consists of three major business capabilities:

Summary Generation

Chat & Q&A

Cost & Usage Tracking

All AI interactions are centralized through the AI Gateway Service.

5. System Components
Component	Responsibility
Kafka	Event transport
Summary Service	Generate case summaries
Chat Service	Conversational interface
AI Gateway Service	Centralized LLM management
Redis	Conversation cache
Summary Database	Summary persistence
Chat Database	Chat history storage
Usage Database	Cost and usage reporting
6. Detailed Design – Summary Generation Service
Purpose
The Summary Generation Service creates AI-generated investigation summaries whenever a case is created or updated.

Inputs
Kafka Event
{
  "caseId": "CASE-1001",
  "eventType": "CASE_CREATED"
}
Processing Workflow
Step 1
Consume case event from Kafka.

Step 2
Retrieve case details.

Step 3
Retrieve customer information.

Step 4
Retrieve payment history.

Step 5
Retrieve session and device activity.

Step 6
Build normalized investigation context.

Step 7
Apply PII redaction.

Step 8
Send request to AI Gateway Service.

Step 9
Validate AI response.

Step 10
Persist summary.

Data Model
{
  "caseId": "CASE-1001",
  "riskScore": 82,
  "alerts": [],
  "transactions": [],
  "sessions": []
}
Reliability
Retry Strategy
Retry 3 times

Exponential backoff

Failure Handling
Failed messages are sent to a Dead Letter Queue.

Idempotency
Key:

caseId + promptVersion
7. Detailed Design – AI Gateway Service
Purpose
The AI Gateway Service centralizes all LLM interactions and abstracts provider-specific implementation details.

Why AI Gateway
Without AI Gateway:

Summary Service --> Azure OpenAI
Chat Service --> Azure OpenAI
With AI Gateway:

Summary Service
      |
Chat Service
      |
      v
AI Gateway
      |
      +--> Azure OpenAI
      +--> Claude
      +--> Gemini
Core Responsibilities
Provider Routing
Selects the most appropriate provider.

Retry Management
Handles:

Timeouts

Temporary failures

Rate limits

Cost Tracking
Tracks:

Tokens

Requests

Cost per model

Failover
Example:

Azure OpenAI
     ↓
Failure
     ↓
Claude
     ↓
Success
Request Lifecycle
Step 1
Receive AI request.

Step 2
Validate payload.

Step 3
Apply model routing policy.

Step 4
Execute prompt.

Step 5
Validate response.

Step 6
Store usage metrics.

Step 7
Return response.

8. Chat Service
Purpose
Allows analysts to interact with case data using natural language.

Example Questions
Why was this customer flagged?

Summarize recent activity.

What transactions increased risk score?

Explain the generated summary.

Workflow
Step 1
Receive analyst request.

Step 2
Load conversation history.

Step 3
Retrieve summary.

Step 4
Build context.

Step 5
Apply PII redaction.

Step 6
Call AI Gateway.

Step 7
Store conversation.

Step 8
Return response.

9. Security Design
Authentication
Microsoft Entra ID

Authorization
Role-Based Access Control (RBAC)

PII Protection
Sensitive data is redacted before AI processing.

Example:

John Smith
becomes

CUSTOMER_NAME
Audit Logging
All AI requests are logged.

10. Monitoring & Observability
Summary Service
Processing latency

Success rate

Failure rate

AI Gateway
Provider usage

Token consumption

Request volume

Cost metrics

Chat Service
Active sessions

Response times

User activity

11. Future Enhancements
Streaming responses

RAG-based document retrieval

Vector search

Prompt versioning

Human feedback loop

Multi-region deployment

12. Conclusion
CasePilot V2 provides a scalable, secure, and AI-enabled investigation platform. The Summary Generation Service automates analyst workflows, while the AI Gateway Service centralizes AI provider interactions and ensures reliability, observability, and cost control.

For the actual submission, use:

Calibri 11

Heading 1: 18 pt Bold

Heading 2: 14 pt Bold

1-inch margins

Company logo on the cover page

Architecture diagram on a dedicated page

Automatic table of contents

This will read like a professional HLD rather than an AI-generated assignment.