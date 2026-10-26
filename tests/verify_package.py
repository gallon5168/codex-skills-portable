from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--manifest', default='manifest/portable-skills-manifest.json'); a=p.parse_args()
root=Path(__file__).resolve().parents[1]; data=json.loads((root/a.manifest).read_text(encoding='utf-8'))
if data.get('mode') != 'portable': print('BASELINE FAIL mode=source-only missing portable repo_path fields'); raise SystemExit(2)
bad=[]
def fs_path(path: Path) -> str:
    value=str(path.resolve())
    return '\\\\?\\'+value if os.name=='nt' and not value.startswith('\\\\?\\') else value
for item in data['files']:
    path=root/item['repo_path']
    if not os.path.isfile(fs_path(path)): bad.append(f"missing:{item['repo_path']}"); continue
    h=hashlib.sha256()
    with open(fs_path(path),'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    h=h.hexdigest()
    if h != item['portable_sha256']: bad.append(f"hash:{item['repo_path']}")
if bad: print(f"MODIFIED FAIL files={len(data['files'])} errors={len(bad)} first={bad[0]}"); raise SystemExit(1)
print(f"MODIFIED PASS files={len(data['files'])} hashes=ok sanitized={sum(bool(x.get('sanitized')) for x in data['files'])}")
