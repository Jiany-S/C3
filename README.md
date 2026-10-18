# CedarBridge Learning Studio

C3 assignment — EECE 503P/798S, Agentic Systems, Fall 2026.

CedarBridge is a fictional student project coaching business. Its assistant, Mira, answers questions about services, collects contact details for requested follow-ups, and records feedback or questions the business sources cannot answer.

[Watch the demonstration video](https://drive.google.com/file/d/1V--RXECcvz5hUiluAs0msjgPW3UpY67B/view?usp=sharing) · [Notebook](business_agent.ipynb) · [Verification report](docs/compliance_report.md)

## Run locally

Use Python 3.11 or later. From the project folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Add your own `OPENAI_API_KEY` to `.env`, then start the app:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the localhost URL printed in the terminal, normally `http://127.0.0.1:7860`. Each conversation has its own history. The classroom evidence panel shows the current turn's route, tool calls, returned observations, and reflection.

Open `business_agent.ipynb` with the same Python environment and run its cells in order. Keep the notebook beside the supplied modules and `me/` folder. By default, it loads the sources, displays the implementation, runs the tests, and builds the interface. Set `RUN_LIVE=true` or `RUN_UI=true` in `.env` to enable the optional live API check or notebook server launch.

Messages sent through the assistant use the OpenAI API and incur API charges. Routing and replies use `gpt-4.1-mini`; reflection uses `gpt-4.1`. Both are configurable in `.env`. Set `ENABLE_REFLECTION=false` to disable review. API keys, runtime logs, and the virtual environment are excluded from Git.

## Design

1. The assistant loads `me/about_business.pdf` and `me/business_summary.txt` as its factual sources.
2. A model call routes each message to general questions, lead collection, or feedback and unknown questions.
3. The selected handler receives the conversation history and available tool schemas. When the model requests a tool, Python validates the arguments, executes it, and returns the observation to the model.
4. The model produces a reply using that observation. A separate reflection call checks the draft against the business facts and tool results before the final answer is shown.

Persona and instructions are separate blocks in `prompts.py` and in the notebook. The persona defines Mira's identity, tone, vocabulary, and values. The instructions define factual grounding, follow-up collection, and tool-use rules.

The two tools are `record_customer_interest(email, name, message)` and `record_feedback(question)`. They write JSONL records under `logs/` and return a success flag and record ID. [Tool contracts](docs/tools.md) document their inputs and outputs. The schemas use OpenAI function calling; the project does not run an MCP server.

Conversation memory covers the latest 24 user/assistant messages. A recorded lead is a request for staff follow-up; it does not book an appointment or send an email.

## Project files

| File | Purpose |
|---|---|
| `business_agent.ipynb` | Assignment walkthrough and executable demonstration |
| `agent.py` | Routing, model requests, tool execution, memory, and reflection |
| `prompts.py` | Persona, instructions, and prompt assembly |
| `app.py` | Gradio interface |
| `me/` | Business PDF and summary; `summary.txt` is an identical compatibility copy |
| `tests/` | Automated checks for orchestration, validation, and error handling |
| `evidence/` | Saved test results, fictional API demonstrations, and reflection checks |

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe scripts/execute_notebook.py
.\.venv\Scripts\python.exe scripts/smoke_gradio.py
```

The recorded checks passed: 50 automated tests, all 11 notebook code cells, and the Gradio HTTP/queue smoke check. These use scripted model responses and do not require an API key. GitHub Actions runs the same checks without live API calls.

The saved [real API demonstration](evidence/demo/README.md) passed 12 route/tool checks. The [reflection checks](evidence/reflection_check/results.json) preserved four correct drafts and corrected two deliberately incorrect drafts. These are controlled fixtures, rather than naturally occurring chatbot failures. Earlier failed runs remain in the evidence folder for comparison.

To repeat the live checks with your own API key:

```powershell
.\.venv\Scripts\python.exe scripts/run_live_demo.py
.\.venv\Scripts\python.exe scripts/check_live_reflection.py
```

## Limits and deployment

Routing, response quality, and reflection depend on the model; the saved cases do not cover every possible input. Memory is limited to the current session. JSONL storage is intended for a local, single-process demonstration. It has no calendar, payment system, email service, or CRM integration. Use fictional contact details when testing: messages go to OpenAI, and local traces can contain those details.

Reflection is included as the optional bonus. Hugging Face Spaces deployment was attempted, but the account was not eligible for the selected free hardware. No hosted app is claimed; the provider responses are saved in `evidence/space_deployment.json`.
