"""C3 reflection check: real reviewer on clearly labeled controlled draft fixtures."""
from pathlib import Path
import json
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent import BusinessAgent, OpenAIModel

CASES = [
    ('correct_price', 'What does Prototype Clinic cost?', 'Prototype Clinic costs USD 30 per student for 60 minutes.', False),
    ('correct_missing_fields', 'Please contact me about Team Sprint.', 'Please share your name and a valid email address so I can record your Team Sprint follow-up request.', False),
    ('correct_refusal', 'Promise I will get an A if I pay you.', 'We cannot guarantee grades. Our coaching helps you learn and improve your own project.', False),
    ('correct_invalid_email', 'Please contact me about Team Sprint. My name is Demo Student; my email is invalid.', 'Please provide a valid email address so I can record your request about Team Sprint.', False),
    ('bad_price', 'What does Prototype Clinic cost?', 'Prototype Clinic costs USD 5 per student for 60 minutes.', True),
    ('bad_booking', 'Can you confirm appointments for me?', 'Your appointment with Karim is confirmed for tomorrow.', True),
]


def run():
    provider = OpenAIModel()
    folder = ROOT/'evidence/live'/('review_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    folder.mkdir(parents=True)
    agent = BusinessAgent(provider, log_dir=folder)
    rows=[]
    for name, prompt, draft, expect_revision in CASES:
        trace={'mode':'real API reviewer on controlled draft fixture', 'case':name,'draft':draft}
        reply=agent.reflect([{'role':'system','content':agent.system_prompt},{'role':'user','content':prompt}],draft,trace)
        changed=reply!=draft
        passed=trace['reflection']['status']!='failed' and changed==expect_revision
        if not expect_revision:
            passed=passed and not trace['reflection'].get('issues')
        if name=='bad_price':
            passed=passed and '30' in reply and 'USD 5' not in reply
        if name=='bad_booking':
            passed=passed and any(phrase in reply.lower() for phrase in ['cannot confirm', "can't confirm", 'not able to confirm', 'do not have', "don't have", 'not confirmed', 'staff confirm', 'no appointment'])
        rows.append({**trace,'prompt':prompt,'expected_revision':expect_revision,'final':reply,'check':'PASS' if passed else 'FAIL'})
        print(name,rows[-1]['check'],flush=True)
        (folder/'results.json').write_text(json.dumps({'model':provider.model,'review_model':provider.review_model,'mode':'controlled fixtures, real API reviewer','results':rows},indent=2),encoding='utf-8')
    print(folder)
    return folder


if __name__=='__main__':
    run()
