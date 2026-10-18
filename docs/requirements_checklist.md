# Source-based requirements and phase boundary

Reviewed 18 October 2026. Local PDFs are authoritative; no claim is made about accessing the Drive URLs. Source paths and SHA-256 hashes are in `source_manifest.json`. Extracted text is an ignored local reading aid, not material to upload with the submission.

## C3 mandatory checklist

The three-page C3 assignment has numbered tasks and a submission checklist, but **no numeric rubric or point allocations**.

| ID | Source | Requirement | Planned evidence |
|---|---|---|---|
| C3-01 | p1, task 1 | Invent name, mission, services, team, unique value | PDF and summary, source-loading test |
| C3-02 | pp1,3 | `me/about_business.pdf`, `business_summary.txt` | Files and PDF visual check |
| C3-03 | p1 task 1 | Task text also names `summary.txt` | Identical compatibility copy in `me/` |
| C3-04 | p2 task 2 | Clearly separate persona and instructions in notebook | Labeled notebook cells and prompts.py |
| C3-05 | p2 task 3 | Classify before answering: general / lead / feedback & unknown | Router decisions, route-specific tool declarations, semantic live matrix |
| C3-06 | p2 task 4 | Exact `record_customer_interest(email,name,message)` | Schema, dispatch, saved name/email/notes, actual API tool event |
| C3-07 | p2 task 4 | `record_feedback(question)` on unknown answers | Schema, dispatch, feedback JSONL, actual API tool event |
| C3-08 | p2 task 4 | Push/print/file logging and MCP-style schema documentation | Persistent JSONL and tools.md (name/input/output); no actual MCP server required |
| C3-09 | p2 task 5 | Assemble persona/instructions/sources into system prompt | Code and notebook displayed prompt |
| C3-10 | p2 tasks 5-6 | In-character, grounded in PDF AND TXT; encourage lead contacts | Prompt, live answer review, partial lead follow-up |
| C3-11 | p2 task 6 | OpenAI or Gemini; model receives input/history/tools | Official SDK adapter and request boundary tests |
| C3-12 | p2 task 6 | Detect calls, execute, return observations, then answer | Tool call IDs and observation messages; tests/live traces |
| C3-13 | p2 task 7 | Working Gradio ChatInterface | Real startup/HTTP/queue probe and live UI check |
| C3-14 | pp1,3 | Main executable `business_agent.ipynb`, dependencies, local .env excluded | Fresh-kernel notebook run, pinned packages, gitignore checks |
| C3-15 | p3 submission | GitHub repository with video showcasing functionality | Requires repository publication and recorded video; local code alone cannot satisfy |
| C3-16 | p3 submission | Runs successfully | Tests + live model + Gradio + notebook evidence |

## C3 optional bonuses

- p2 task 8: actual model reflection before final answer; log original and revised replies. A passing mock is implementation evidence; a live unchanged review does not demonstrate live self-correction.
- p3: Hugging Face Spaces deployment, described as a smaller bonus. Not required, and external deployment needs the user's approval. Local JSONL is not durable across arbitrary hosted restarts.

## Additional user-requested quality work

- Small modular Python implementation, app.py, `.env.example`, README, automated tests, demo matrix, exact video script, strict compliance report.
- Test invalid input, missing contact fields, errors after successful tool writes, memory isolation, API failures, reflection failure, and real Gradio queue startup.
- Use modern `OpenAI().chat.completions.create` rather than obsolete `openai.ChatCompletion`. This preserves the assignment's API, message/history/tool semantics; document that compatibility choice.
- No secrets, real contact data, caches, virtualenvs, or fabricated results in submission.
- Do not begin C4 until explicit approval of C3.

## C4 planning checklist ONLY - implementation not authorised

| ID | Source | Mandatory requirement / evidence needed later |
|---|---|---|
| C4-01 | p1 + p2 2.1 | Extend business project; specify goal, audience, tools, limitations |
| C4-02 | p1 | Use exactly one supported framework: LangGraph, CrewAI, AutoGen, OpenAI Agents SDK; no prebuilt AgentExecutor |
| C4-03 | p2 2.2 | Manual ReAct: system behavior/tool descriptions, explicit model action detection, execution, observation return, repeated cycle, final-answer parsing |
| C4-04 | p2 2.3 | At least two personas with different task roles, tone, vocabulary, response style, values, and matching LLM configuration; test both |
| C4-05 | p2 2.3 | Controlled with/without CoT-style prompting comparison |
| C4-06 | p2 2.3 | Controlled zero-shot/few-shot comparison |
| C4-07 | p2 2.3 | Controlled system/in-message instruction comparison |
| C4-08 | p2 2.3 | Vary supported model parameters; record configurations and compare actual performance |
| C4-09 | pp2-3 2.4 | Dedicated instructions, single-purpose steps, explicit inputs/outputs, worked example, no persona conflicts |
| C4-10 | p3 2.5 | Reflection: most helpful/natural persona |
| C4-11 | p3 2.5 | Reflection: best prompt/configuration combination |
| C4-12 | p3 2.5 | Reflection: reasoning and tool usage quality |
| C4-13 | p3 2.5 | Reflection: observable instruction effects |
| C4-14 | p3 2.5 | Reflection: biggest implementation challenges |
| C4-15 | p3 | Include reflection in notebook or PDF; working assistant and real logged experiments |

C4 grading: use case/write-up 10; manual ReAct 30; persona prompt/configuration 20; configuration experiments/comparison 15; clear instructions 10; creativity/clarity/reflection 15 (total 100). No explicit C4 bonus is listed. The PDF does not specify a video requirement or exact notebook filename for C4; do not invent one as a professor requirement.

Dependencies: preserve the fictional fact sheet, tool contracts and logs from C3. C4 can later replace orchestration with explicit LangGraph nodes and conditional edges. Tentative roles are a welcoming service advisor and a careful technical scoping coach; no C4 personas, graph, experiments, or reflection answers have been implemented. Re-read all C4 materials after approval.

## Course concepts informing C3

C3 notes pp5-9 and deck slides 41-69 distinguish fixed routing from model-driven action. This project deliberately combines a routing workflow with a model-controlled bounded tool loop; the router alone is not called autonomous reasoning. Memory is short-term per-session chat, while local business sources ground responses. Persistent leads/feedback are business records, not a learning system or a cross-session personal memory. Reflection follows the evaluator/optimizer pattern, with one review call, not a guarantee of correctness.

C4 notes pp1-9 and deck cover generation parameters, persona vs. instructions, single-purpose instruction design, CoT/ToT/GoT/ReAct, and frameworks. Those inform planning only. Provider parameter support must be verified before C4 experimentation; not every provider supports top-k or penalties.
