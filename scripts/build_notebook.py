"""Generate a readable notebook; runtime code stays in one tested Python source."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def markdown(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code(source):
    return {"cell_type": "code", "metadata": {}, "source": source.splitlines(True),
            "execution_count": None, "outputs": []}


def build():
    cells = [
        markdown("""# CedarBridge Learning Studio - C3 Business Assistant
EECE 503P/798S, Agentic Systems, Fall 2026. Fictional classroom business.

This notebook is the main teaching/demo entry point. Run all cells from a fresh Python 3.11+ kernel after installing `requirements-dev.txt` in the project environment. Keep this notebook with the supplied Python modules and `me/` folder. For Colab, upload/extract the complete C3 folder and set the working directory to it; a notebook uploaded alone lacks its business sources.

The default run loads both sources, shows the actual implementation, executes deterministic tests, and builds Gradio. It makes **no paid calls** unless `RUN_LIVE=true`; it launches a server only if `RUN_UI=true`. These flags are execution controls, not simulated model behavior. The code displayed below comes from the same modules used by app.py, so tests and UI share one implementation.

## 1. Business and goal
Mira explains project coaching services, collects requested follow-up leads, and records feedback or unknown policies. Target audience: university students building their own projects. No university affiliation, calendar, payments, email sending, ghostwriting, or guaranteed grades. See the profile for authoritative fictional facts.

The C3 routing workflow selects a handler. Within that handler, the LLM decides whether to call a tool; Python executes the action and returns the observation. This is a limited tool-using agent, not reinforcement learning or a full planning system. C4 has not been started."""),
        code("""from pathlib import Path
import os, sys, json, inspect, subprocess
from IPython.display import display, Markdown, Code

if not (Path.cwd() / 'agent.py').exists() and (Path.cwd() / 'C3/agent.py').exists():
    os.chdir('C3')
assert Path('agent.py').exists(), 'Run from the complete C3 project folder.'
sys.path.insert(0, str(Path.cwd()))
from dotenv import load_dotenv
load_dotenv('.env')  # No secret values are displayed.
from agent import (BusinessAgent, Tools, JsonLog, OpenAIModel, ModelError,
                   TOOL_SCHEMAS, load_business, normalize_history)
from prompts import PERSONA, INSTRUCTIONS, ROUTER_INSTRUCTIONS, system_prompt
knowledge = load_business()
print('Loaded both PDF and TXT business sources.')
display(Markdown(Path('me/business_summary.txt').read_text(encoding='utf-8')))"""),
        markdown("## 2. PERSONA - identity, tone, vocabulary and values\nThis block defines who Mira is."),
        code("print(PERSONA)"),
        markdown("## 3. INSTRUCTIONS - operational rules\nThis separate block defines what Mira does, when tools are appropriate, and where her authority ends."),
        code("print(INSTRUCTIONS)"),
        markdown("## 4. System prompt assembly and factual grounding\nBoth the TXT summary and extracted PDF text are injected into the system context. The tiny fact sheet fits directly in context; a vector database would add unnecessary complexity."),
        code("""assembled_system_prompt = system_prompt(knowledge)
assert all(label in assembled_system_prompt for label in
           ['PERSONA', 'INSTRUCTIONS', '[business_summary.txt]', '[about_business.pdf]'])
display(Code(inspect.getsource(system_prompt), language='python'))
print('System prompt characters:', len(assembled_system_prompt))"""),
        markdown("## 5. Classify before answering: three-way router\nAn actual JSON-mode model call chooses general, lead, or feedback using the sources and recent history. Price-only interest is general; missing policies are feedback; short contact replies continue a lead. Mixed lead/feedback uses the lead branch, where both tools are available. Scripted tests verify branch behavior; the real API matrix is needed to assess semantic accuracy."),
        code("""print(ROUTER_INSTRUCTIONS)
display(Code(inspect.getsource(BusinessAgent.route), language='python'))"""),
        markdown("## 6. Tool schemas and persistent actions\nThe declarations use JSON Schema with name, description, required parameters and no additional fields. `docs/tools.md` documents success/error outputs. They are MCP-style descriptions for this assignment, not a live MCP server. The exact required standalone functions are also exposed in agent.py. Calls are validated, written as JSONL and returned as structured observations."),
        code("""print(json.dumps(TOOL_SCHEMAS, indent=2))
display(Code(inspect.getsource(Tools), language='python'))"""),
        markdown("## 7. Model, memory, tool execution and final answer\nThe maintained `OpenAI().chat.completions.create` method replaces the assignment's older `openai.ChatCompletion` syntax while retaining its intended message/history/tools flow. Each session's recent 24 user/assistant messages provide short-term memory; within each turn, tool calls and observations remain in the model context. There is no global shared conversation history. A bounded loop prevents unending actions, and errors after successful writes return record IDs. Keys come from the local environment and are never printed."),
        code("""display(Code(inspect.getsource(OpenAIModel), language='python'))
display(Code(inspect.getsource(normalize_history), language='python'))
display(Code(inspect.getsource(BusinessAgent.respond), language='python'))"""),
        markdown("## 8. Optional reflection bonus\nOne separate model call reviews the actual draft and tool observations. Traces store the original, brief policy findings, actual returned revision and whether the answer changed. A failed review retains the draft with an explicit failure status in the trace. Reflection is not a proof of factual accuracy and cannot retroactively execute a missing tool."),
        code("display(Code(inspect.getsource(BusinessAgent.reflect), language='python'))"),
        markdown("## 9. Run deterministic tests\nThese checks use scripted responses for model behavior, and installed SDK types at the API boundary. They prove Python orchestration, validation, memory and failure handling. They do not prove real model routing or tool selection."),
        code("""result = subprocess.run([sys.executable, '-m', 'pytest', 'tests', '-q'], capture_output=True, text=True)
print(result.stdout)
if result.returncode:
    print(result.stderr)
assert result.returncode == 0, 'Fix test failures before demonstrating.'"""),
        markdown("## 10. Real API verification (opt in)\nSet OPENAI_API_KEY locally, set RUN_LIVE=true, then rerun this cell. It runs the twelve-case demonstration matrix with fictional contact data and writes real observations to ignored `evidence/live/`. Review the actual answers as well as automatic route/tool checks. No prefilled responses are presented as model executions."),
        code("""if os.getenv('RUN_LIVE', 'false').lower() == 'true':
    from scripts.run_live_demo import run
    live_folder = run()
    print('Review results:', live_folder / 'results.json')
else:
    print('NOT RUN in this notebook execution: real API matrix. Set RUN_LIVE=true to opt in.')"""),
        markdown("## 11. Gradio ChatInterface\nThe same code is used by `python app.py`. Start locally with RUN_UI=true. For an explicitly chosen Colab run, change launch settings as needed and review public sharing before enabling it. Starting the UI does not prove API access; send the demo interactions and inspect actual tool records."),
        code("""from app import build_demo
demo = build_demo()
if os.getenv('RUN_UI', 'false').lower() == 'true':
    demo.launch(server_name='127.0.0.1', share=False, prevent_thread_lock=True)
else:
    print('ChatInterface built; server launch disabled (RUN_UI=false).')
    demo.close()"""),
        markdown("""## 12. Evidence, limitations and submission
Read `docs/compliance_report.md` for actual outcomes and requirement-by-requirement status, `evidence/` for verification artifacts, and `docs/video_demo_plan.md` for exact recording interactions.

Limits: semantic routing and notes/consent interpretation are model-dependent; a 12-case matrix is not exhaustive. Reflection is also model-dependent and may miss mistakes. Local file logging is for one process; hosted restarts may lose records. User chat is transmitted to OpenAI; local traces contain contact information, so use invented demo data and exclude logs from Git. History truncation can lose older contact details, in which case Mira should ask again. A newly restarted chat has no previous session memory.

Submit a GitHub repository plus an actual video. Confirm keys, logs, virtual environments and course PDFs are excluded. Spaces deployment is optional and has not been authorized. This is the mandatory C3 review checkpoint: **do not start C4 until the user explicitly approves C3.**"""),
    ]
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"}}, "nbformat": 4, "nbformat_minor": 5}
    for i, cell in enumerate(cells):
        cell['id'] = f"c3-{i:02d}"
    (ROOT / 'business_agent.ipynb').write_text(json.dumps(notebook, indent=1), encoding='utf-8')
    print('Built executable teaching notebook')


if __name__ == '__main__':
    build()
