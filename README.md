\# ShieldAgent - Autonomous A2A Security \& Budget Guardrail



A lightweight, production-ready security gateway and cost-observability router designed for the Nasiko Agent-to-Agent runtime.



\## Core Capabilities

\- \*\*A2A Routing:\*\* Dynamic dispatch for conversational and transactional tasks.

\- \*\*Security Interception:\*\* Real-time regex and semantic detection of prompt injection and credential leaks.

\- \*\*Cost \& Cascade Limits:\*\* Halts recursive agent execution before token budgets are exceeded.

\- \*\*OpenTelemetry Telemetry:\*\* Emits structured traces capturing trace IDs, span latency, and token attribution.



\## Demo Video

\- \[Watch the 90-Second Demo](https://www.loom.com/share/0573aacec50e48bfa077c0e35b19459e)



\## Setup \& Run Locally

```bash

pip install fastapi uvicorn pydantic

python main.py

