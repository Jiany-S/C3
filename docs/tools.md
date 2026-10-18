# Tool contracts (MCP-style documentation)

These are JSON Schema function declarations passed to OpenAI's native tool interface, following the class's MCP-style schema presentation. This is **not** a running MCP server or implementation of MCP transport/discovery. `agent.TOOL_SCHEMAS` is the executable schema source.

## record_customer_interest(email, name, message)

Purpose: persist one customer-requested staff follow-up in `leads.jsonl`.

Input object: required strings `email`, `name`, `message`; additional keys rejected. Email must resemble a valid address (not proof of delivery), at most 254 characters. Name is nonempty, at most 120 characters, without newlines. Notes are nonempty, at most 3000 characters. Model dispatch also checks that the name and email occur in this user's recent messages. The prompt requires a follow-up request and real customer-provided notes; intent/consent interpretation remains model-dependent.

Success observation:
```json
{"ok": true, "record_id": "generated UUID", "kind": "leads", "storage": "local JSONL"}
```

Saved record: generated `id`, UTC ISO `timestamp`, `email`, `name`, `message`. Returns no appointment, payment, or email-send status because none occurred.

## record_feedback(question)

Purpose: persist customer feedback or an unanswered business question in `feedback.jsonl`.

Input object: required string `question`, nonempty, at most 4000 characters; additional keys rejected.

Success observation:
```json
{"ok": true, "record_id": "generated UUID", "kind": "feedback", "storage": "local JSONL"}
```

Saved record: generated `id`, UTC ISO `timestamp`, `question`.

## Shared failure and dispatch behavior

Invalid arguments or failed local writes return `{"ok": false, "error": "safe descriptive message"}`. Invalid JSON, unknown tool names, extra fields and tools disallowed by the route are rejected before dispatch. Failed saves do not return success IDs. Observations are JSON-serialized into `role=tool` messages with the model's original `tool_call_id` before the next completion.

General: feedback tool available for grounding misses. Lead: both tools available, so mixed requests can be handled. Feedback: feedback tool required on the first model response; a successful observation is required before returning the normal final reply.

The loop permits at most five model steps and four tool calls per step. Identical calls in one turn reuse the existing observation to prevent duplicate writes. This is single-process file logging with a thread lock; no multi-worker durability or cross-turn retry idempotency is claimed. A network failure after a write returns the saved record ID so the user does not assume the action was lost.

`traces.jsonl` stores mode (mock/live), original request, router decision, tool requests/observations, draft, review findings, revision status, final answer, and safe errors. It contains potentially private conversation details. All runtime logs are ignored by Git; use invented contacts in demonstrations.
