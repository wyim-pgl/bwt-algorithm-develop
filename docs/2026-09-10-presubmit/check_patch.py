"""Apply the reviewed patch, or verify current bytes and replay from its git baseline.
Default is read-only verification. --apply requires every target's original bytes.
Run from the repository root. No result payloads, commits or jobs are generated.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');args=p.parse_args()
patch=json.loads(Path(__file__).with_name('patch.json').read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def replay(before,entry):
    s=before.decode('utf-8')
    assert digest(before)==entry['before_sha256'],entry['path']
    for op in reversed(entry['ops']):
        assert s[op['start']:op['end']]==op['old'],entry['path']
        s=s[:op['start']]+op['new']+s[op['end']:]
    after=s.encode('utf-8');assert digest(after)==entry['after_sha256'],entry['path']
    return after
if args.apply:
    head=subprocess.check_output(['git','rev-parse','--short=7','HEAD']).decode().strip()
    assert head==patch['baseline_commit'],(head,patch['baseline_commit'])
    pending=[]
    for entry in patch['files']:
        path=Path(entry['path']);assert not path.is_absolute() and '..' not in path.parts
        pending.append((path,replay(path.read_bytes(),entry)))
    # All targets validated before the first write; refuse unrelated prior edits.
    for path,after in pending:path.write_bytes(after)
    print('APPLIED:',len(pending),'files; no commit/staging/rehash performed')
else:
    replayed=0
    for entry in patch['files']:
        actual=Path(entry['path']).read_bytes();assert digest(actual)==entry['after_sha256'],entry['path']
        if entry['path']=='resume.md':continue  # ignored file: apply preflight bound original bytes
        before=subprocess.check_output(['git','show',patch['baseline_commit']+':'+entry['path']])
        assert replay(before,entry)==actual,entry['path'];replayed+=1
    print(f'PASS: {len(patch["files"])} final hashes; {replayed} tracked files replay byte-identically from baseline; ignored resume checked by final hash')
