"""Publish the reviewed package only after explicit user deployment approval.

No paid hardware/plan operations. Tokens and API key are never printed.
"""
from pathlib import Path
import hashlib
import json
import os
import secrets

from dotenv import dotenv_values
from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Jiany-S/cedarbridge-c3'


def deploy(hardware='cpu-basic'):
    folder=ROOT/'tmp/space_upload'
    manifest=json.loads((ROOT/'evidence/space_package.json').read_text(encoding='utf-8'))
    actual=sorted(str(p.relative_to(folder)).replace('\\','/') for p in folder.rglob('*') if p.is_file())
    assert actual==manifest['files']
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest, 'Refresh the reviewed package first.'
    key=dotenv_values(ROOT/'.env').get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('Project OpenAI key is not configured.')
    api=HfApi()
    assert api.whoami()['name']==REPO.split('/')[0], 'Unexpected Hugging Face account.'
    # cpu-basic has no hourly charge; a provider plan restriction fails without buying anything.
    assert hardware in {'cpu-basic','zero-a10g'}, 'Only hardware without an hourly compute charge is allowed.'
    url=api.create_repo(REPO, repo_type='space', space_sdk='gradio', space_hardware=hardware, private=False, exist_ok=False)
    password=secrets.token_urlsafe(24)
    credentials=ROOT/'tmp/space_credentials.txt'
    credentials.write_text('URL: https://huggingface.co/spaces/'+REPO+'\nUsername: professor\nPassword: '+password+'\n', encoding='utf-8')
    api.add_space_secret(REPO,key='OPENAI_API_KEY',value=key)
    api.add_space_secret(REPO,key='SPACE_ACCESS_PASSWORD',value=password)
    api.add_space_variable(REPO,key='OPENAI_MODEL',value='gpt-4.1-mini')
    api.add_space_variable(REPO,key='OPENAI_REVIEW_MODEL',value='gpt-4.1')
    commit=api.upload_folder(repo_id=REPO,repo_type='space',folder_path=str(folder),commit_message='Deploy verified C3 CedarBridge classroom assistant')
    result={'repo_id':REPO,'url':str(url),'source_commit':commit.oid,'hardware_requested':hardware,'hourly_compute_upgrade':False,
        'app_auth':'password protected','api_key_storage':'private Space secret','credentials_file':'tmp/space_credentials.txt','status':'uploaded; runtime verification pending'}
    (ROOT/'evidence/space_deployment.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approved',action='store_true',help='Use only after the user approves this deployment.')
    parser.add_argument('--hardware',choices=['cpu-basic','zero-a10g'],default='cpu-basic')
    args=parser.parse_args()
    if not args.approved:
        parser.error('Explicit deployment approval is required. Preparation alone does not publish.')
    deploy(args.hardware)
