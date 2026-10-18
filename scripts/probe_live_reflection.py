"""Optional C3 diagnostic: real reviewer, explicitly injected flawed draft.

This is not a naturally generated failure or a C4 experiment.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent import BusinessAgent, OpenAIModel


def run(folder):
    provider = OpenAIModel()
    agent = BusinessAgent(provider, log_dir=folder)
    draft = "Prototype Clinic costs USD 5, and your appointment is now confirmed."
    messages = [{"role": "system", "content": agent.system_prompt},
                {"role": "user", "content": "What does Prototype Clinic cost?"}]
    trace = {"mode": "real API reviewer; intentionally injected flawed draft",
             "draft": draft, "model": provider.model}
    revised = agent.reflect(messages, draft, trace)
    trace["final"] = revised
    Path(folder).mkdir(parents=True, exist_ok=True)
    (Path(folder) / 'reflection_probe.json').write_text(json.dumps(trace, indent=2), encoding='utf-8')
    print(json.dumps(trace, indent=2))


if __name__ == '__main__':
    run(ROOT / 'evidence/live/reflection_probe')
