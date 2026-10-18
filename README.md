---
title: CedarBridge Learning Studio
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 6.30.0
app_file: app.py
pinned: false
---

# CedarBridge Learning Studio - C3

Mira is a business assistant for a fictional student project coaching studio. She answers from a PDF and summary, collects customer-requested follow-up leads, and logs feedback or unpublished business questions. This is the standalone C3 submission for EECE 503P/798S, Fall 2026. C4 is not implemented and requires explicit approval first.

## Install (Python 3.11+)

From this C3 directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Edit `.env` locally, adding `OPENAI_API_KEY`. Keep it out of chat, videos and Git. The default model is `gpt-4.1-mini`, configurable with `OPENAI_MODEL`; an alternative must support Chat Completions, function tools, JSON mode, temperature and the output-token setting. `requirements.txt` contains runtime dependencies; `requirements-dev.txt` adds tests/notebook execution/PDF rebuilding. The tested Windows dependency snapshot is `evidence/environment.txt`; direct dependencies are pinned while transitive dependencies are resolved by pip.

The application makes paid API calls only when a message is sent (or the live demo runner is explicitly run). One ordinary turn normally uses a router call, answer call, optional tool/observation calls and a reflection call. Reflection can be disabled with `ENABLE_REFLECTION=false`. No key is needed for deterministic tests or to start the UI, but actual model replies require one.

## Run Gradio

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the printed localhost URL, normally `http://127.0.0.1:7860`. Start a new chat to clear conversational context. `gr.ChatInterface` supplies that session's history; there is no shared global chat history. A missing key produces an explicit setup message, not a simulated business answer. The UI is local (`share=False`).

## Run the notebook

Open `business_agent.ipynb` in Jupyter or a notebook editor, selecting the `.venv` Python interpreter. If using an existing Jupyter installation, optionally register it with:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --user --name cedarbridge-c3
```

Alternatively, verify every cell without a notebook editor:

```powershell
.\.venv\Scripts\python.exe scripts/execute_notebook.py
```

The notebook is executable with the complete C3 project alongside it; it imports and displays the actual tested code rather than maintaining a second implementation. Run All shows the business, distinct PERSONA and INSTRUCTIONS blocks, system prompt assembly, router, schemas, tools, API integration, memory, loop, reflection and tests. Paid API execution and UI launch are opt-in (`RUN_LIVE=true`, `RUN_UI=true` in `.env`). The verifier explicitly disables both so a fresh-kernel validation is safe and reproducible. Upload/extract the whole project if using Colab, change directory to C3, install dependencies there, and configure the key securely. The default localhost launch is intended for local Jupyter; public Colab sharing is a separate user decision.

## Business files

- `me/about_business.pdf`: full fictional profile: mission, services/prices, team, value proposition and boundaries.
- `me/business_summary.txt`: concise factual summary, loaded with the PDF on every new agent initialization.
- `me/summary.txt`: identical copy covering a filename inconsistency in the assignment task text.
- `scripts/build_business.py`: shared fact sheet and reproducible PDF/TXT builder; requires development dependencies.

All staff, prices and services are invented. CedarBridge has no university affiliation. It helps students learn; it does not ghostwrite assignments or promise grades.

## How the agent works

1. A JSON-mode LLM router examines the latest message, recent history and business sources **before** response generation.
2. General questions receive a source-grounded handler with the feedback tool available for an overlooked unknown. Lead requests get a collection handler with both tools. Feedback/unknown questions get a handler that requires a feedback tool call before normal completion.
3. The model emits native function calls. Python validates the name, JSON fields and values, executes permitted functions, then appends an observation with the matching tool-call ID.
4. The model uses that observation to answer or recover. Five model steps limit each turn. Identical tool calls within one turn reuse the saved observation.
5. Optional reflection reviews the draft against facts and tool outcomes, then returns a real revised or unchanged reply. Original/review/revision/error statuses are logged.

`prompts.py` separates identity from operational policy. `agent.py` contains the implementation. `app.py` is a small Gradio entry point. [Tool contracts](docs/tools.md) describe exact schemas and outputs. MCP-style JSON schemas are documented; no actual MCP server is claimed. The code uses the maintained `OpenAI().chat.completions.create` method instead of the old `openai.ChatCompletion` example in the assignment ([official API reference](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create), [function calling flow](https://developers.openai.com/api/docs/guides/function-calling)). Gradio's callback receives message and history as documented in [ChatInterface](https://gradio.app/docs/gradio/chatinterface).

## Logs and memory

Default `logs/` (override with `LOG_DIR`) contains `leads.jsonl`, `feedback.jsonl`, and `traces.jsonl`. Saves return actual IDs and structured observations. A lead is a **local follow-up request**, not an appointment, sent email, payment, or CRM entry. Invalid inputs return errors and are not saved. Tool errors after earlier successful writes retain the earlier record IDs in the user-facing error.

Recent 24 user/assistant messages are short-term memory; current tool calls and observations remain in context for the turn. Persistent logs do not train the model or provide cross-session customer recall. Chat content is sent to OpenAI; local traces may include contact information. Use invented names and `example.com` addresses in demos. Logs are ignored by Git. Stop the app and delete demo logs manually when no longer needed; the prototype has no retention or customer-deletion interface.

## Tests and actual demonstration

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q --junitxml=evidence/pytest.xml
.\.venv\Scripts\python.exe scripts/smoke_gradio.py
.\.venv\Scripts\python.exe scripts/run_live_demo.py
```

The first command uses **scripted model outputs** and installed SDK types. It tests source loading, three actual branches, missing/invalid arguments, lead/feedback writes, observation return, memory isolation, API errors, step limits and reflection. It cannot establish model intelligence. The second runs a real Gradio HTTP server and queue/API with a clearly labeled **mock model callback**. The third uses **real OpenAI calls** and invented data; it saves twelve realistic cases plus raw tool/reflection traces under ignored `evidence/live/<UTC timestamp>/`. Its route/tool checks are automatic; answers still need human quality review.

See [verification status and strict self-evaluation](docs/compliance_report.md), the [requirements checklist](docs/requirements_checklist.md), and [exact video script](docs/video_demo_plan.md). The reviewed real API run is preserved in [evidence/demo](evidence/demo/README.md); actual browser screenshots and traces are in `evidence/browser/`. Do not infer a live pass from a mocked test. Evidence records actual outcomes and limitations.

## Submission and optional deployment

The C3 PDF requires a **GitHub repository and demonstration video**. Record the interactions in the video plan, upload the video using your preferred permitted method, and put the real video link here before submission. **Video: not recorded yet.** Publish only the C3 project; do not upload keys, runtime logs, the virtual environment, notebook checkpoints or the professor's course PDFs. Inspect `git status --ignored` before pushing. Source hashes in `docs/source_manifest.json` document the local materials reviewed without copying them into the repository.

Hugging Face Spaces is an optional smaller bonus and has not been deployed. README metadata and app.py provide a starting point. Before an approved deployment, change the bind address to `0.0.0.0`, store the key as a Space secret, and decide how to preserve/restrict lead data: local files alone are not durable hosted storage. Do not expose this classroom prototype publicly with real customer data.

## Known limitations

- Semantic routing, intent/consent interpretation, note extraction and factual responses depend on the model. Exact name/email provenance is checked, but substring presence is not an identity or ownership check.
- Reflection can miss problems, and an API/review failure may leave the original draft unchanged. It cannot perform missing actions retroactively. No guarantee of live self-correction is made without a corresponding actual trace.
- The recent-history window can forget older lead details. Tool results from earlier turns are represented by user-visible replies, not replayed as persistent structured tool memory.
- JSONL logging is single-process with a thread lock, not a concurrent production database. Duplicate retries across separate turns can create duplicate leads; only identical calls within a turn are deduplicated.
- No live calendar, payment gateway, email service, CRM, official university data or external knowledge search is connected.
- The assignment has no numeric C3 rubric; no numerical grade is invented. GitHub publication and a real video remain separate submission requirements.

**C3 review checkpoint: C4 work is not authorized until the user explicitly approves C3.**
