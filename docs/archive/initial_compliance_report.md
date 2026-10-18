# C3 strict compliance report

Reviewed 18 October 2026, after re-reading all three pages of the local C3 assignment from beginning to end. See `requirements_checklist.md` and `source_manifest.json` for source paths, page references, hashes and the separate C4 planning checklist. No C4 implementation was started.

**Assessment: the local C3 application is implemented and working, with actual API/browser evidence. The submission is not yet complete because the GitHub publication and required video remain.** The C3 PDF gives no numeric grading rubric, so a numerical grade would be invented. All technical requirements below pass within the tested scope; that is not a guarantee of performance on arbitrary conversations.

## Requirement-by-requirement evidence

Notebook cell IDs are stable metadata IDs visible in the `.ipynb` JSON; the corresponding numbered section headings are visible in Jupyter. The notebook displays the actual imported implementation rather than duplicating it. It executes independently from a fresh kernel **with the complete project files present**, not as a notebook-only upload.

| ID | Requirement | Implementation / notebook evidence | Verification | Status |
|---|---|---|---|---|
| C3-01 | Fictional identity: name, mission, services, team, value | `scripts/build_business.py:SECTIONS`, `me/` files; notebook section 1, cell c3-01 | `test_load_both_sources`; visual review of full one-page PDF | PASS |
| C3-02 | Required PDF and summary | `me/about_business.pdf`, `me/business_summary.txt`; `agent.load_business` | Both appear in actual system context; PDF rendered and checked for legibility/clipping | PASS |
| C3-03 | Filename discrepancy in task text | `me/summary.txt`, identical to business_summary.txt | Byte equality in source test | PASS |
| C3-04 | Distinct persona and instructions | `prompts.PERSONA`, `prompts.INSTRUCTIONS`; notebook c3-03 / c3-05 | Fresh-kernel notebook prints each under its own heading; prompt assembly assertion | PASS |
| C3-05 | Three-way router before handling | `BusinessAgent.route/respond`, `ROUTE_POLICY`; notebook section 5, c3-09 | `test_three_real_branches`, malformed classifier tests; final real matrix 12/12 expected routes | PASS |
| C3-06 | Exact lead tool; name/email/notes | `agent.record_customer_interest`, `Tools.record_customer_interest/execute`; notebook section 6, c3-11 | Actual lead call in final `demo/traces.jsonl`, saved lead f50fe285-4bbb-46b4-aadd-b002fc5c82e7; successful lead/invalid input/provenance tests; browser follow-up | PASS |
| C3-07 | Unknown-question and feedback tool | `agent.record_feedback`, `Tools.record_feedback`; notebook c3-11 | Four actual final matrix feedback records; refund policy, explicit suggestion, scholarship and availability; browser refund record | PASS |
| C3-08 | Logging and MCP-style schemas | `TOOL_SCHEMAS`, `JsonLog`, `docs/tools.md`; notebook c3-11 | Actual JSONL records and observations; schema/dispatch validation tests | PASS |
| C3-09 | Assemble system prompt | `prompts.system_prompt`, `BusinessAgent.__init__`; notebook c3-07 | Assertion for PERSONA/INSTRUCTIONS/PDF/TXT; actual source-backed answers | PASS |
| C3-10 | Character, grounding, encourage contact | `INSTRUCTIONS`, route-specific policies; notebook sections 2-5 | Agent review of actual twelve answers in `evidence/demo/quality_review.json`; known prices, unknown policies, refusal, grade-promise rejection | PASS with model-dependent limits |
| C3-11 | Permitted API, input/history/tools | `OpenAIModel.complete`, `normalize_history`; notebook section 7, c3-13 | Installed SDK request/type tests; actual gpt-4.1-mini completions; history reaches router and generation | PASS |
| C3-12 | Detect, execute, return tool observations; final answers | `BusinessAgent.respond`, `Tools.execute`; notebook c3-13 | Matching call IDs and structured observations; real persisted records; loop-limit, duplicate, storage and post-write API failure tests | PASS |
| C3-13 | Working gr.ChatInterface | `app.build_demo`; notebook section 11, c3-21 | Real HTTP/config/queue smoke test; four actual browser interactions with real OpenAI and both tools | PASS |
| C3-14 | Executable notebook, dependencies, local key excluded | `business_agent.ipynb`, requirements files, `.env.example`, `.gitignore` | All 11 code cells executed in fresh project kernel; tests passed; dependency check clean; Git inclusion audit | PASS |
| C3-15 | GitHub repo and video | Local Git project prepared; `docs/video_demo_plan.md` specifies exact interactions | Local screenshots and traces exist, but no GitHub remote publication or recorded video is claimed | PARTIAL - user steps remain |
| C3-16 | Runs successfully | Notebook + app + provider adapter + tools | 47 tests, 12-case real API run, real Gradio queue and browser, fresh notebook | PASS in tested local environment |

The SDK syntax is intentionally modernized from the PDF's old `openai.ChatCompletion` example to `OpenAI().chat.completions.create`, preserving the required behavior. Source grounding uses both complete small documents directly in context. The assignment asks for MCP-style schema documentation, not a networked MCP server; no MCP transport is claimed.

## Actual verification outcomes

| Check | Outcome | Scope / artifact |
|---|---|---|
| Full automated suite | **47 passed**, 20.12 seconds | `evidence/pytest.xml`; scripted model behavior + installed SDK types + real Gradio construction |
| Fresh notebook run | **11/11 code cells executed** | `evidence/notebook_execution.json`; real imports, deterministic tests, no paid notebook calls/server launch |
| Dependency consistency | **No broken requirements** | `python -m pip check`; installed versions in `evidence/environment.txt` |
| Gradio HTTP/config/queue | **PASS** | `evidence/gradio_smoke.json`; real server and client, deliberately mock model callback |
| Final real API matrix | **12/12 route/tool checks passed** | gpt-4.1-mini, UTC run 20261018T104346Z; `evidence/demo/results.json`, actual traces and saved records |
| Real browser + API | **Four interactions passed** | `evidence/browser/verification.json`, screenshots, traces; factual answer, multistep lead, memory plus unknown policy |
| PDF layout | **PASS** | One page rendered with Poppler and visually checked; no clipped text or overlapping sections |
| Real API outage/error injection | **NOT TESTED live** | Safe errors, malformed router outputs, storage failures and post-write failures tested with mocks; no deliberate invalid-key/provider-outage calls |
| Human review | **PENDING** | `human_quality_review` fields in raw results intentionally remain pending; Codex's separate manual review is labeled as such |

The final API matrix saved exactly **one fictional lead and four feedback records**. It took 53.45 seconds total for twelve turns (approximately 2.7-7.3 seconds per turn in that run). This is one observation per case, not a statistically reliable benchmark. The browser run separately saved one fictional lead and one feedback record. API calls incurred the configured provider's normal usage; no cost estimate is invented without billing evidence.

### Final actual demo matrix

| Case | Actual route | Actual successful tools | Functional result |
|---|---|---|---|
| Prototype Clinic price/duration | general | none | USD 30 / 60 minutes, grounded |
| Interest in prices only | general | none | USD 60 Team Sprint, no unintended lead |
| Staff follow-up, missing name/email | lead | none | Asks for missing contacts, retains supplied notes |
| Name/email follow-up | lead | record_customer_interest | Saves supplied identity and previous project notes |
| Which service did I ask about? | general | none | Recalls Prototype Clinic / API project |
| Unpublished refund policy | feedback | record_feedback | Admits missing policy and acknowledges save |
| Explicit evening-session suggestion | feedback | record_feedback | Acknowledges actual feedback save |
| Known price + unknown scholarship | feedback | record_feedback | Correct price; scholarship described as unpublished |
| Karim tomorrow at 14:00 | feedback | record_feedback | No calendar invented; saves question |
| Decline contact, ask hours | general | none | Correct hours, no lead save |
| Invalid email | lead | none | Requests valid email, no invalid record; minor extra clarification |
| Override rules / promise an A | general | none | Rejects grade guarantee, stays in role |

## Bonus evidence and quality limits

**Reflection is implemented and actually exercised.** The final matrix logged nine unchanged reviews, two revisions with reported issues, and one issue-free rephrasing. These are observable edits, not proof that the reviewer improved every answer. Some natural review findings were overcritical or redundant: one complained about requesting name/email even though those fields were missing; another added a project-note clarification. The user-facing results stayed usable, but reflection quality should not be oversold.

The separate `evidence/demo/reflection_probe.json` is stronger evidence of factual correction: a **deliberately injected** draft said USD 5 and claimed a confirmed appointment; a real API reviewer corrected the price to USD 30 and removed the booking claim. This was a diagnostic of the real reviewer, not a naturally generated agent failure and not a C4 experiment. The initial mock regression also demonstrates correction/error paths, clearly labeled as mock.

**Spaces: NOT IMPLEMENTED/NOT DEPLOYED.** README metadata is preparation only. User approval and a hosting/data-storage decision are still required before deployment. The optional smaller bonus is not claimed.

## Strict critique and resolved failures

- **Complexity:** one provider adapter, one router, one bounded native tool loop, two tools and one optional review. No vector database, agent framework, or unnecessary service. The notebook imports/displays the same implementation as the app to avoid drift. The supporting evidence is more extensive than a minimal class submission because reproducibility and independent review were requested.
- **Routing:** the first live run passed 11/12 route/tool checks but failed to save a complete lead because the assistant demanded more project notes. The prompt now treats short supplied notes as sufficient; final live run and browser follow-up saved the lead. Price-only interest, mixed known/unknown questions, refusal and conversational follow-up were tested. Semantic accuracy outside this small English set is not established; Arabic dialogue, extreme ambiguity and long histories remain untested.
- **Actual tool use:** both tools were genuinely requested by the model, executed and persisted. Definitions alone are not counted as proof. Validation blocks missing/extra fields and fabricated names/emails. Consent and note interpretation still depend on the model, and substring provenance is not identity verification.
- **Provider integration:** modern installed SDK and real calls passed. Keys are loaded from the environment and excluded. API timeout/quota/authentication/error handling is mocked, not live outage-tested. The default model must be accessible to the user's account; arbitrary model overrides may not support the same parameters.
- **Conversation continuity:** actual history-based lead collection and recall passed. A minor redundant project-note request remains in the invalid-email scenario. History is deliberately finite and cross-session recall is not claimed.
- **Business grounding:** final prices/durations/hours matched the sources. An earlier draft treated unpublished scholarships as categorically unavailable; wording was corrected and the final live answer preserved uncertainty. No calendar/booking/email/grade guarantees were fabricated in the final evidence.
- **Error handling:** malformed JSON, forbidden tools, invalid inputs, disk failures, empty responses, API errors and a post-write provider failure were tested. Saved actions retain their IDs on later errors. Reflection failures are visible in traces and do not pretend to be successful reviews.
- **Reflection:** an early validator discarded harmless issue-free edits; this is fixed and such edits are labeled `rephrased`. Raw returned review JSON is retained. The final run had no failed review, but its critique still contains false positives. The injected factual-error probe supports correction capability; it does not establish universal reliability.
- **Environment:** sandboxed Gradio checks blocked at asyncio socketpair creation. They were stopped and rerun successfully with local networking enabled. Earlier installation failures and incomplete-dependency test attempts are not presented as app successes.
- **Writing:** the business includes specific service durations/prices, responsibilities and operational limits. The notebook explains the course concepts in terms of the actual implementation. The user should still review the explanations and be prepared to explain the code in their own words.
- **Evidence/submission:** real API traces, real browser screenshots, an executable notebook and a video script exist. Screenshots are not a video. No GitHub publication or Spaces deployment is claimed.

## Remaining user actions and C3 checkpoint

1. Inspect the notebook, sources, screenshots and actual results; try the running local Gradio app or launch it with the README command.
2. Record the required video using `docs/video_demo_plan.md`; replay it and verify both model-called tools are visible. No screen-recording capability was available in this browser interface, so a recording was not fabricated.
3. Publish the prepared local repository to your chosen GitHub repository and add the actual video link in README. Repository destination/visibility and video hosting are your decisions. Never add `.env`, virtualenvs, logs, caches or course PDFs.
4. Decide whether the optional Spaces bonus is worth doing. It has not been deployed and is not required for C3.
5. Approve C3 explicitly before any C4 implementation begins. **Work stops at this review checkpoint.**
