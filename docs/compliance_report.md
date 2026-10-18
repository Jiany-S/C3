# C3 verification report

Checked against the C3 assignment on 18 October 2026.

The project implements the required business assistant, notebook, router, two tools, conversation history, and Gradio interface. The demonstration video is linked in the [README](../README.md).

## Assignment requirements

| Requirement | Implementation and evidence |
|---|---|
| Fictional business: mission, services, team, and value | `me/about_business.pdf` and `me/business_summary.txt` |
| Separate persona and instructions | `prompts.py`; notebook sections 2 and 3 |
| Assemble the system prompt from persona, instructions, PDF, and summary | `system_prompt()`; notebook section 4 |
| Route general questions, leads, and feedback before answering | `BusinessAgent.route()`; 12 real API cases in `evidence/demo/results.json` |
| Record requested customer interest | `record_customer_interest(email, name, message)`; saved fictional lead and tool observation |
| Record feedback and unanswered questions | `record_feedback(question)`; saved fictional feedback and observations |
| Document tool names, inputs, and outputs | `docs/tools.md` and `TOOL_SCHEMAS` |
| Pass input, history, and tools to the model | `OpenAIModel.complete()` and `BusinessAgent.respond()` |
| Execute tool calls and return observations before the final reply | `Tools.execute()`; matching tool-call IDs in saved traces |
| Gradio ChatInterface | `app.py`; HTTP/queue smoke check and recorded demonstration |
| Executable notebook and dependencies | `business_agent.ipynb`, `requirements.txt`, and `requirements-dev.txt` |
| Repository and functionality video | `https://github.com/Jiany-S/C3`; Drive video linked in README |
| Local API key excluded from upload | `.env.example` and `.gitignore` |

## Recorded checks

| Check | Result | Scope |
|---|---|---|
| Automated suite | 50 passed | Scripted model responses; orchestration, schemas, validation, memory, storage, and error paths |
| Notebook | 11/11 code cells executed | Fresh kernel; live API calls and server launch disabled |
| Dependency check | Passed | No broken installed requirements |
| Gradio smoke check | Passed | Real HTTP server and queue with a mock model callback |
| Real API demonstration | 12/12 route/tool checks passed | Fictional data; saved replies and observations in `evidence/demo/` |
| Reflection | 6/6 controlled checks passed | Four correct drafts preserved; incorrect price and booking drafts corrected |

The final API run used `gpt-4.1-mini` for routing/replies and `gpt-4.1` for review. Earlier runs are retained. The smaller reviewer sometimes rewrote valid clarifications, which led to the separate reviewer configuration. Review provenance is recorded in `evidence/demo/quality_review.json`; it is not student or instructor approval.

## Demonstration video

The student-recorded demonstration covers the business profile, persona and instructions, a service question, lead collection, conversation memory, an unpublished policy question, feedback logging, tool observations, controlled reflection results, and the test result. The edit preserves the original responses and results.

The video shows the successful lead acknowledgement, but does not expand its raw tool observation or the general-question route label. Those are available in the saved API evidence. Some long reflection JSON lines extend outside the recorded editor viewport. The recording also contains the student's contact details.

## Bonuses and limits

Reflection is implemented and demonstrated with logged drafts and revised replies. The deliberately incorrect reflection inputs are labeled controlled fixtures. The ordinary replies in the final API matrix passed review unchanged.

The Hugging Face bonus is incomplete. CPU Basic and ZeroGPU deployment attempts received HTTP 402 eligibility responses. No Space is deployed, no purchase was made, and no secrets were uploaded.

The tests establish behavior for the recorded scenarios, rather than exhaustive model reliability. Arabic conversations, long histories, and repeated statistical trials were not evaluated. Live provider outages were not deliberately triggered; error handling was checked with injected failures. JSONL logging is local and single-process, and hosted restarts would not provide durable storage. The assistant cannot book appointments, send email, take payments, or guarantee grades.
