# System Context Diagram

```mermaid
flowchart LR

    Analyst[Analyst]

    CasePilot[CasePilot]

    CaseSystem[Case Management System]
    UserSystem[Customer Systems]
    PaymentSystem[Payment Systems]
    SessionSystem[Session Systems]

    AzureOpenAI[Azure OpenAI]
    Claude[Claude]
    Gemini[Gemini]

    Analyst --> CasePilot

    CasePilot --> CaseSystem
    CasePilot --> UserSystem
    CasePilot --> PaymentSystem
    CasePilot --> SessionSystem

    CasePilot --> AzureOpenAI
    CasePilot --> Claude
    CasePilot --> Gemini
```
