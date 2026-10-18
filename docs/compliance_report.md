# C3 regrade and verification report

Reviewed again on **18 October 2026**, using the complete local three-page C3 assignment, its chapter notes and lecture material. The source paths/hashes and detailed C3/C4 planning checklist remain in `source_manifest.json` and `requirements_checklist.md`. C4 implementation is still not authorized and has not begun.

**Regrade: all mandatory technical requirements pass within the tested scope. Reflection is implemented and demonstrated. The Spaces bonus was attempted with approval but is blocked by Hugging Face account eligibility. GitHub publication and the actual student-recorded video are still required before submission is complete.** The professor provides no numerical C3 rubric, so no numerical grade is invented. A working tested system is not a claim of perfection on arbitrary model inputs.

The previous audit is preserved in `archive/initial_compliance_report.md`; it is historical, not the current result.

## Requirements checked against implementation and actual evidence

The notebook's stable cell IDs are listed below along with its visible section headings. It uses the tested modules supplied in the complete project, rather than a second divergent implementation.

| ID | Requirement (C3 PDF) | Exact implementation / notebook section | Proof | Status |
|---|---|---|---|---|
| C3-01 | Name, mission, services, team, unique value (p1) | `scripts/build_business.py:SECTIONS`; `me/about_business.pdf`; notebook section 1 / c3-01 | Source-loading test; entire business PDF visually checked | PASS |
| C3-02 | PDF plus business summary (pp1,3) | `me/about_business.pdf`, `me/business_summary.txt`; `agent.load_business` | Both source labels present in assembled prompt; source tests | PASS |
| C3-03 | Task text's alternate summary filename (p1) | `me/summary.txt` compatibility copy | Exact byte-equality test with business_summary.txt | PASS |
| C3-04 | Clearly separate persona and instructions (p2) | `prompts.PERSONA/INSTRUCTIONS`; notebook c3-03 / c3-05 | Fresh notebook prints both separately | PASS |
| C3-05 | General / lead / feedback router before handling (p2) | `BusinessAgent.route/respond`, `prompts.ROUTE_POLICY`; notebook c3-09 | Branch tests; final real 12-case matrix and exact browser rehearsal | PASS |
| C3-06 | `record_customer_interest(email,name,message)` (p2) | Standalone named function and `Tools.record_customer_interest/execute`; notebook c3-11 | Actual model call, returned observation and lead JSONL; missing/invalid input tests | PASS |
| C3-07 | `record_feedback(question)` on unknown answers (p2) | Standalone named function and `Tools.record_feedback`; notebook c3-11 | Actual refund/suggestion/scholarship/availability saves; browser evidence | PASS |
| C3-08 | Persistent logging and documented MCP-style schemas (p2) | `JsonLog`, `TOOL_SCHEMAS`, `docs/tools.md`; notebook c3-11 | Schema/dispatch tests and actual saved JSONL observations | PASS |
| C3-09 | Assemble system prompt from persona/instructions/sources (p2) | `prompts.system_prompt`, `BusinessAgent.__init__`; notebook c3-07 | Prompt assembly assertion; both PDF/TXT loaded | PASS |
| C3-10 | Business character, factual grounding, contact encouragement (p2) | `INSTRUCTIONS`, route handlers | Reviewed real answers: correct prices/hours, missing policies acknowledged, no grade/booking guarantees | PASS within tested prompts |
| C3-11 | OpenAI or Gemini; input, history and tools (p2) | `OpenAIModel.complete`, `normalize_history`; notebook c3-13 | Installed SDK-type tests; real OpenAI requests; history passed to router/generation | PASS |
| C3-12 | Detect calls, execute tools, return observations, generate final answer (p2) | `BusinessAgent.respond`, `Tools.execute`; notebook c3-13 | Matching tool-call IDs and actual persistent records; API/storage/step-limit tests | PASS |
| C3-13 | Gradio ChatInterface (p2) | `app.build_demo` contains an actual `gr.ChatInterface` inside styled `gr.Blocks`; notebook c3-21 | Real HTTP/queue probe and browser interaction; 50-test suite includes UI | PASS |
| C3-14 | Executable notebook, dependencies, local .env excluded (pp1,3) | Notebook, requirements, `.env.example`, `.gitignore` | 11/11 notebook code cells; clean dependency check; secret/exclusion audit | PASS |
| C3-15 | GitHub repository and functionality video (p3) | Local Git project; exact `docs/video_demo_plan.md` | Ready locally; GitHub publication and actual recording not yet done | PARTIAL - user submission steps |
| C3-16 | Runs successfully (p3) | Complete local app/notebook | Automated, real API, reflection and browser evidence below | PASS locally |

The modern `OpenAI().chat.completions.create` syntax preserves the assignment's intended behavior while replacing its old `openai.ChatCompletion` example. MCP-style schemas are documented and exercised through native function calls; this project does not claim to run an MCP server.

## Actual checks, including the new audit

| Check | Actual outcome | Evidence / limits |
|---|---|---|
| Automated suite | **50 passed** | `evidence/pytest.xml`; deterministic scripted model behavior, installed SDK types, real Gradio construction |
| Fresh notebook | **11/11 code cells executed** | `evidence/notebook_execution.json`; paid notebook calls and server launch disabled |
| Dependency consistency | **No broken requirements** | `pip check`; pinned direct dependencies |
| Real Gradio server/queue | **PASS** | `evidence/gradio_smoke.json`; real HTTP and Gradio client with deliberately mock model callback |
| Final real assistant matrix | **12/12 route-and-tool checks passed** | `evidence/demo/results.json`; UTC run 20261018T114513Z; response/router gpt-4.1-mini, reviewer gpt-4.1 |
| Controlled real reflection checks | **6/6 passed** | `evidence/reflection_check/results.json`; four correct drafts preserved, injected wrong price and false appointment corrected |
| Exact video-prompt browser rehearsal | **PASS** | `evidence/review_browser/`; actual UI plus actual API; general, lead, memory, unknown policy and suggestion |
| Business PDF layout | **PASS** | One page rendered and fully visually checked for clipping/overlap |
| Live provider outage/auth/quota errors | **NOT TESTED live** | Error paths are covered by injected/mocked errors; no deliberate invalid-key or provider-outage traffic |
| Spaces deployment | **BLOCKED** | Both approved free hardware attempts received provider HTTP 402; `evidence/space_deployment.json` |

Final real matrix: correct service price/duration; price-only interest without a lead save; lead collection across turns; memory follow-up; refund question; explicit suggestion; known price plus unknown scholarship; specific staff availability; refusal of contact; invalid email; and a request to promise an A. It saved one fictional lead and four feedback records. The run took 39.21 seconds total, about 2.6-4.4 seconds per turn. This is one recorded run per case, not statistical proof of model reliability.

Raw result fields for human review remain pending; `evidence/demo/quality_review.json` is explicitly Codex's inspection, not a claim that the student or professor approved the results.

## What changed after regrading

- **Interface:** responsive studio layout, emerald theme, service cards, a clear send button, downloadable factual profile, and a collapsed classroom evidence panel. The panel receives the trace directly from the current request; it never reads the latest line of a shared log to identify a user's result. It is hidden on Spaces.
- **Lead continuity:** a named desired service already supplies service-interest notes. The assistant can request missing name/email together. The final invalid-email case requests a corrected email without needlessly asking for already supplied name or service.
- **Tool deduplication:** equivalent JSON calls with different whitespace/key order now reuse the same observation within a turn. The new test verifies only one write. Cross-turn retries can still create duplicate records; production idempotency is not claimed.
- **Reflection:** the earlier small reviewer sometimes invented policy violations and rewrote correct clarifications. The review instructions now distinguish user requests from draft text, and the reviewer defaults to `gpt-4.1` (`OPENAI_REVIEW_MODEL`), while normal routing/replies remain on `gpt-4.1-mini`. The final six-case controlled check preserved all four good drafts and corrected both bad drafts. The earlier failed fixtures are retained as development evidence.
- **Honest review logging:** all twelve ordinary replies in the final matrix passed review unchanged. That is a valid reflection outcome, not self-correction evidence. The separate injected-error fixtures demonstrate actual API correction. No injected draft is presented as a naturally generated failure.
- **Hosting preparation:** eight-file allowlist package; key-free source; correct Space bind address; hidden diagnostic panel; password guard. Deployment was actually attempted, and its failure is documented rather than claimed as a bonus pass.

## Both bonuses, strictly assessed

**Reflection: PASS - implemented and demonstrated.** One real model review runs before the reply, with draft, findings, returned revision, reviewer model and final answer logged. In the controlled checks, USD 5 became the published USD 30, and a false appointment confirmation was removed. Four correct drafts remained unchanged. These fixtures exercise the actual reviewer on intentionally supplied drafts; they are not C4 experiments or fabricated live observations. Reflection can still make mistakes outside this small check, and a failed review is explicitly logged while retaining the original draft.

**Hugging Face Spaces: BLOCKED - not earned yet.** The user approved publication of `Jiany-S/cedarbridge-c3` with public source and password-protected app, storing the existing OpenAI key as a private Space secret, on no-cost hardware only. The provider rejected CPU Basic with HTTP 402 requiring PRO, then rejected ZeroGPU with HTTP 402 requiring eligible access (PRO, account eligibility or a grant). A read-only check confirmed the Space does not exist. No purchase occurred and no secrets were uploaded. `scripts/prepare_space.py` and `scripts/deploy_space.py` are ready for eligible access; prepared files or an attempted upload alone do not earn this bonus. A static page would not demonstrate the required working Gradio assistant, so no static substitute is claimed.

## Remaining limits and actions

- No numerical grade: C3 has no published point allocation. The implementation is ready for review; the overall submission is incomplete until GitHub and the video are submitted, and the smaller hosting bonus remains blocked.
- Semantic routing, note/consent interpretation, factual generation and reflection are model-dependent. The current English scenarios passed; exhaustive ambiguity, Arabic conversation, long-history behavior and statistical repeatability have not been established.
- There is no calendar, email service, payment gateway, CRM or official university affiliation. Records are classroom JSONL, not production storage. Hosted local storage would be temporary across restarts/rebuilds.
- The history window is finite and no cross-session personal memory or model learning is claimed. The UI uses per-session history and per-request trace results.
- API errors, malformed tool inputs, disk failures, invalid contacts, step limits and post-write errors were tested. Live outage behavior is not inferred from mocks.
- Keep the key, HF token, any future deployment credentials and runtime logs out of Git and the recording. Fictional example.com demonstration evidence is intentionally included.
- Follow `docs/video_demo_plan.md` for exact camera actions and narration. Record your own actual screen/voice; screenshots are not a video. Add the actual video link to the GitHub README and publish the prepared project to your chosen GitHub repository.
- Arrange eligible Hugging Face access only if you want to pursue the smaller bonus. Nothing has been purchased automatically.
- **Stop at C3. C4 requires a separate explicit approval.**
