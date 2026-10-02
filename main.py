import time
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ShieldAgent: Nasiko Guardrail & A2A Routing Engine",
    description="A2A agent pipeline with OTel trace logging and cost guardrails",
    version="1.0.0"
)

class AgentRequest(BaseModel):
    session_id: str = Field(default="sess_default", description="Conversation session ID")
    prompt: str = Field(..., description="User prompt or incoming agent dispatch")
    max_budget_tokens: int = Field(default=1000, description="Budget guardrail threshold")
    user_role: str = Field(default="customer", description="Access level: 'customer' or 'admin'")

def support_worker_agent(prompt: str) -> str:
    prompt_clean = prompt.lower()
    if "refund" in prompt_clean:
        return "Action: Processed simulated refund claim for standard policy item."
    elif "order" in prompt_clean:
        return "Action: Retrieved order status #98421: In transit, arriving in 2 days."
    return "Action: Standard FAQ response generated."

@app.post("/a2a/route")
async def handle_nasiko_route(payload: AgentRequest):
    start_time = time.time()
    simulated_tokens = len(payload.prompt.split()) * 4 + 150
    estimated_cost_usd = round(simulated_tokens * 0.000002, 6)

    # Guardrail 1: Security Injection Check
    blocked_keywords = ["ignore previous instructions", "drop table", "system prompt", "leak credentials"]
    for keyword in blocked_keywords:
        if keyword in payload.prompt.lower():
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "status": "BLOCKED_SECURITY_VIOLATION",
                "reason": f"Prompt injection pattern detected: '{keyword}'",
                "nasiko_otel_trace": {
                    "trace_id": f"trace_{int(time.time()*1000)}",
                    "span_name": "nasiko.guardrail.security_check",
                    "route_decision": "ABORT",
                    "latency_ms": duration_ms,
                    "tokens_used": simulated_tokens,
                    "cost_usd": estimated_cost_usd
                }
            }

    # Guardrail 2: Budget & Cascade Limit
    if simulated_tokens > payload.max_budget_tokens:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "BLOCKED_BUDGET_OVERRUN",
            "reason": f"Projected tokens ({simulated_tokens}) exceed limit ({payload.max_budget_tokens}).",
            "nasiko_otel_trace": {
                "trace_id": f"trace_{int(time.time()*1000)}",
                "span_name": "nasiko.guardrail.budget_check",
                "route_decision": "BLOCKED",
                "latency_ms": duration_ms,
                "tokens_used": simulated_tokens,
                "cost_usd": estimated_cost_usd
            }
        }

    # Dispatch to downstream agent
    agent_output = support_worker_agent(payload.prompt)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "status": "SUCCESS_EXECUTED",
        "agent_response": agent_output,
        "nasiko_otel_trace": {
            "trace_id": f"trace_{int(time.time()*1000)}",
            "span_name": "nasiko.a2a.dispatch",
            "routed_agent": "support_worker_agent",
            "latency_ms": duration_ms,
            "tokens_used": simulated_tokens,
            "cost_usd": estimated_cost_usd
        }
    }

@app.get("/health")
def health_check():
    return {"status": "active", "service": "ShieldAgent", "nasiko_compatible": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)