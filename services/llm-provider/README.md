# LLM Provider Service

Abstraction layer over external AI providers. Business services never communicate directly with a specific vendor.

## Supported Providers

- Azure OpenAI (primary)
- Anthropic Claude (long-context)
- Google Gemini (multimodal)
- Future providers (pluggable)

## Responsibilities

- Provider routing and failover
- Circuit breaker and retry logic
- Cost optimization across providers
- Token usage logging
