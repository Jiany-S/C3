# C3 video: exact steps to record

Suggested length: 5-6 minutes. This is a practical target, not a duration specified by the professor. Record your screen and your voice. The video must be an actual demonstration; do not substitute these instructions or screenshots for a recording.

## Before pressing Record

- Open PowerShell in `C:\Users\jijos\Desktop\EECE 503P\C3`.
- If the app is not already running, run `.\.venv\Scripts\python.exe app.py`.
- Open `http://127.0.0.1:7860` in a full browser window. Use a fresh chat. Leave **Classroom evidence · latest turn** collapsed initially.
- Open three other tabs/windows: `me/about_business.pdf`, `business_agent.ipynb`, and `evidence/reflection_check/results.json`.
- Open `docs/compliance_report.md` if you want the verification summary ready.
- Close `.env`, Hugging Face tokens/settings, deployment credentials, unrelated chats and other private windows. Use only the invented identity below. Never show the access password while recording.
- If a Space has been deployed successfully, sign into its app before recording and have its URL ready. Claim this bonus only if `evidence/space_deployment.json` says the runtime was verified, not merely uploaded.
- Choose your screen area and microphone in your recording software. Do a ten-second sound/readability test first.

## What to do on camera, in order

- **1. Introduce the project (about 15 seconds).** Show the app home screen. Say: “This is CedarBridge Learning Studio, a fictional student project coaching business. Mira answers business questions, collects requested leads, and records feedback or unanswered questions.”

- **2. Show the factual sources (about 20 seconds).** Switch to `about_business.pdf`. Point briefly to the mission, services, fictional team, and limits. Then show `me/business_summary.txt` in the project. Say: “The assistant loads both this PDF and this summary as its business knowledge.” Do not read the entire PDF aloud.

- **3. Show persona versus instructions (about 25 seconds).** Switch to notebook sections **2. PERSONA** and **3. INSTRUCTIONS**. Say: “Persona defines Mira's identity and communication style. Instructions define grounding, missing information, contact collection, and tool-use rules.” Briefly show section **4. System prompt assembly**.

- **4. Demonstrate the general route (about 25 seconds).** Return to the app and send exactly:
  ```text
  What does Prototype Clinic cost, and how long is it?
  ```
  Wait for the reply. Check that it says **USD 30 per student** and **60 minutes**. Expand **Classroom evidence · latest turn**. In the execution record, show `route.intent = general` and an empty `tool_events` list. Say: “This is a grounded answer; no record-writing tool is needed.” Collapse the evidence panel.

- **5. Start a lead conversation (about 20 seconds).** Send exactly:
  ```text
  Please have staff contact me about Prototype Clinic for my API project.
  ```
  Mira should ask for the missing **name and valid email**. Say: “The router selected lead collection. The service notes are already in the conversation, so the assistant asks for the missing contact fields.”

- **6. Complete the lead and prove the actual tool execution (about 35 seconds).** Send exactly:
  ```text
  My name is Demo Student and my email is demo.student@example.com.
  ```
  Wait for the reply. Expand the evidence panel. Show `route.intent = lead`, `record_customer_interest`, the arguments, and its observation with `ok = true` and a generated `record_id`. Show `logs/leads.jsonl` if needed to prove persistence. Say: “The model requested the tool, Python saved the record, and the observation was returned to the model. This is a follow-up request, not a confirmed appointment or sent email.” Collapse the panel.

- **7. Prove conversation memory (about 15 seconds).** Send exactly:
  ```text
  Which service did I ask staff about?
  ```
  The reply should recall **Prototype Clinic for the API project** without you repeating it. Say: “The assistant uses this session's conversation history.” Do not create another lead record for this question.

- **8. Demonstrate an unanswered question (about 30 seconds).** Click **Clear** to start a new chat, then send:
  ```text
  What is your refund policy?
  ```
  The reply should say the policy is **not published**, and acknowledge that the question was recorded. Expand the evidence panel. Show `route.intent = feedback`, `record_feedback`, and `ok = true`. Say: “The assistant acknowledges the missing policy instead of inventing one and records the unanswered question.”

- **9. Demonstrate explicit feedback (about 20 seconds).** Collapse the panel, then send:
  ```text
  Feedback: please add evening coaching sessions.
  ```
  Show the acknowledgement and the current turn's successful `record_feedback` observation. Optionally show the new `logs/feedback.jsonl` line. Say: “The same feedback tool handles a suggestion as well as an unanswered business question.”

- **10. Show the reflection bonus honestly (about 35 seconds).** Show the current turn's `draft`, `reflection`, and `final` in the evidence panel. If its review is unchanged, say so. Then open `evidence/reflection_check/results.json` and show the **bad_price** case: the deliberately injected draft says USD 5, the real reviewer reports the error, and the returned revision says USD 30. Briefly show **bad_booking**, where a false confirmed appointment is removed. Say: “These are controlled bad drafts supplied to the actual API reviewer. They demonstrate self-correction; I am not claiming that the assistant naturally produced these errors.” The **correct_price** or **correct_invalid_email** cases also show that correct drafts are preserved. Do not describe a stylistic rephrasing as a factual correction.

- **11. Show validation (about 20 seconds).** Show the latest test result and the compliance report. If you want to run tests on camera, use:
  ```powershell
  .\.venv\Scripts\python.exe -m pytest tests -q
  ```
  State the actual reported pass count. Explain: “Automated tests use scripted model outputs. The separate live matrix and browser traces demonstrate actual API behavior.” Do not call mocked tests live model verification.

- **12. Show the Spaces bonus only after successful deployment (about 20 seconds).** Open the actual Hugging Face Space URL and demonstrate one question there. Keep the browser address visible so hosting is clear. Explain that the app is password protected and its key is stored as a private Space secret. Do not show the password or secrets page. If deployment is pending or blocked, omit the claim and state that the smaller hosting bonus has not been completed.

- **13. Close (about 10 seconds).** Show the project files. Say: “The repository contains the notebook, business sources, application, dependencies, tests, and actual evidence. The API key is excluded. This is the standalone C3 project.”

## After recording

- Replay the video: check your voice, readable text, complete responses, both successful tool observations, and reflection evidence.
- If anything differs from the checkpoints, keep the actual result and rerun after fixing it. Never narrate a save or deployment that did not happen.
- Upload the actual video through a service allowed by your course and add its real link to the GitHub README. The assignment does not specify a hosting platform.
- Submit the GitHub repository and video as instructed. C4 remains on hold until you explicitly approve C3.
