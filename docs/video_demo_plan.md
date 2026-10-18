# Video demonstration script (about 4 minutes)

Record an actual run; this script is a plan, not a recording. Use screen recording on your computer (for example Windows Snipping Tool's record mode or OBS). Capture the notebook and local browser, with your voice explaining the steps. Keep `.env`, API dashboard, other browser tabs and real contacts out of the frame.

1. **0:00-0:30, identity and architecture.** Open the business PDF and notebook. Say: "CedarBridge is a fictional student project coaching business. Mira uses this PDF and summary. Persona defines her identity; instructions define actions and boundaries." Show the two labeled notebook blocks.
2. **0:30-0:55, general route.** In Gradio send: `What does Prototype Clinic cost, and how long is it?` Check USD 30 and 60 minutes against the source. Show the matching live route trace, labeled general.
3. **0:55-1:40, lead and memory.** Send: `Please have staff contact me about Prototype Clinic for my API project.` The assistant should ask for missing name/email. Then send: `My name is Demo Student and my email is demo.student@example.com.` Show the actual `record_customer_interest` call, observation ID, and the new lead JSONL line. Explain that a local request was recorded, not an appointment or email. Send: `Which service did I ask staff about?` Show context continuity.
4. **1:40-2:15, unknown answer.** Start a new chat; send: `What is your refund policy?` Show the missing-policy acknowledgement, `record_feedback` call, returned observation and saved feedback line.
5. **2:15-2:40, explicit feedback.** Send: `Feedback: please add evening coaching sessions.` Show the second saved feedback record. Send `Please do not contact me. Just tell me your service hours.` to show a known answer without creating a lead.
6. **2:40-3:15, bonus reflection.** Show an actual trace's draft, issues and revised_response. If the live review left the reply unchanged, state that plainly. A unit-test injected bad draft demonstrates correction logic but must be labeled MOCK, not a live correction. Do not claim a live rewrite without one in the trace.
7. **3:15-3:45, validation and limitations.** Show the test summary and live results, identifying mocked vs. actual model checks. Explain no calendar/payment/email service, no official university advice, finite session memory, and model-dependent routing. Show the safe response to an invalid email if time allows.
8. **3:45-4:00, submission.** Show the repository files and notebook. Confirm the key is locally configured and excluded. Explain that C4 is waiting for approval.

Before upload: replay the video, check text is readable, verify both tools visibly executed and responses are audible, remove accidental secret exposure, and put the video link in the GitHub README (or attach the video as the professor instructs). The assignment does not prescribe a video duration or hosting service; four minutes is a practical suggestion.

During recording, inspect JSONL in your editor or run `Get-Content logs/leads.jsonl -Tail 1`, `Get-Content logs/feedback.jsonl -Tail 2`, and `Get-Content logs/traces.jsonl -Tail 1` from C3. Only show invented demo records.
