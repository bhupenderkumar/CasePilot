# Summary Consumer

Kafka consumer that orchestrates automated case summary generation.

## Responsibilities

- Consumes case events from Kafka
- Aggregates data from User, Payment, and Session services
- Orchestrates PII redaction, context building, and LLM summarization
- Stores generated summaries in PostgreSQL
- Routes failed events to Dead Letter Queue (DLQ)
