# Actual API evidence

`results.json`, `traces.jsonl`, `leads.jsonl` and `feedback.jsonl` are unchanged copies of the final real OpenAI run (gpt-4.1-mini, UTC 20261018T114513Z). Only fictional contacts and example.com addresses were used. `provenance.json` includes file hashes. User/human review fields are still pending; `quality_review.json` is explicitly Codex's inspection, not a claim of human approval.

`initial_results.json` preserves the first real run's failed lead collection (11/12 automatic checks). Later prompt/validation fixes and their final results are described in the compliance report. The preserved failure prevents an expected result being passed off as an execution.

`reflection_probe.json` is a real API review of a deliberately injected incorrect draft. It demonstrates factual correction, but is not a naturally generated conversation error. Final natural reviews are in the traces; not every edit is an improvement.

To reproduce with your own key: `python scripts/run_live_demo.py`. New raw runs go into ignored `evidence/live/`. Do not automatically publish future raw logs if they contain real contacts or sensitive information.
