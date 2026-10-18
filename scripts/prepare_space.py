"""Prepare a small reviewed upload folder; never publish or include credentials."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
FILES = ['app.py', 'agent.py', 'prompts.py', 'requirements.txt',
         'me/about_business.pdf', 'me/business_summary.txt', 'me/summary.txt']
README = """---
title: CedarBridge Learning Studio
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 6.30.0
python_version: 3.12
app_file: app.py
pinned: false
---

# CedarBridge Learning Studio

A fictional student project coaching business assistant for EECE 503P/798S C3.

Mira uses a business PDF and summary, classifies messages into general questions,
lead requests or feedback/unknown questions, executes native OpenAI tool calls,
and reviews her draft before replying. No university affiliation or guaranteed grades.

The owner provides classroom demo credentials separately. Use invented contacts only.
Chat is sent to OpenAI. Tool records and diagnostic traces are stored in the Space's
temporary local filesystem; records may be lost on a rebuild/restart. No emails,
bookings or payments are sent. This is an academic demonstration, not a production CRM.

Required secrets in Space Settings: OPENAI_API_KEY and SPACE_ACCESS_PASSWORD.
Optional variables: OPENAI_MODEL (default gpt-4.1-mini), OPENAI_REVIEW_MODEL (default gpt-4.1), SPACE_ACCESS_USER (default professor).
Reflection is enabled by default. The classroom trace viewer is hidden on Spaces.
"""


def prepare():
    folder = ROOT / 'tmp/space_upload'
    folder.mkdir(parents=True, exist_ok=True)
    # An allowlist, never an upload of the whole project or its .env/logs.
    for name in FILES:
        dest = folder / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    (folder / 'README.md').write_text(README, encoding='utf-8')
    actual = sorted(str(p.relative_to(folder)).replace('\\', '/') for p in folder.rglob('*') if p.is_file())
    assert actual == sorted(FILES + ['README.md']), 'Unexpected files in upload folder; inspect before deployment.'
    manifest = {'files': actual, 'sha256': {n: hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in actual},
        'credentials_in_package': False, 'published': False,
        'proposed_repo': 'Jiany-S/cedarbridge-c3', 'hardware': 'cpu-basic or eligible free ZeroGPU; no paid hardware or plan purchase',
        'visibility': 'public source; application password protected', 'secrets_required': ['OPENAI_API_KEY','SPACE_ACCESS_PASSWORD']}
    (ROOT/'evidence/space_package.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))
    return folder


if __name__ == '__main__':
    prepare()
