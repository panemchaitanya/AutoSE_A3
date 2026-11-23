"""Reproducible behavioral checks of local E2 fixtures, no provider calls.

Added after E2 to retain the previously ephemeral development probes.
A reported failure below confirms the planted behavior violates its issue.
Not hidden acceptance tests, and not a rerun of E2 model reviews.
"""
from pathlib import Path
import subprocess,tempfile,json
ROOT=Path(__file__).resolve().parents[2]
PIN='edff96aeb2616402e9489d46e90a592c05565621'
PROBES={
'sp1':'''db.insert_multiple([{'x':1},{'x':2},{'x':3}]); got=len(db.search(Q.x.exists(),limit=1)); print(json.dumps({'expected':1,'actual':got,'defect_confirmed':got!=1}))''',
'sp2':'''db.insert({'x':1}); got=db.get(Q.x==9,default='missing'); print(json.dumps({'expected':'missing','actual':got,'defect_confirmed':got!='missing'}))''',
'sp3':'''from tinydb.operations import increment
v={'n':0.5}; increment('n')(v); print(json.dumps({'expected':1.5,'actual':v['n'],'defect_confirmed':v['n']!=1.5}))''',
'sp4':'''n=db.insert({'x':1}); removed=db.remove(doc_ids=[str(n)]); print(json.dumps({'expected_remaining':0,'actual_remaining':len(db),'removed':removed,'defect_confirmed':len(db)!=0}))''',
'sp5':'''db.insert_multiple([{'x':0},{'x':0},{'x':1},{'x':1}]); got=len(db.search(Q.x==1,limit=2)); print(json.dumps({'expected':2,'actual':got,'defect_confirmed':got!=2}))''',
}
results=[]
for seed,code in PROBES.items():
 with tempfile.TemporaryDirectory(prefix='autose-seed-verify-') as temp:
  subprocess.run(['git','-C',str(ROOT),'worktree','add','--detach',temp,PIN],check=True,capture_output=True)
  try:
   subprocess.run(['git','-C',temp,'apply',str(Path(__file__).parent/seed/'diff.patch')],check=True,capture_output=True)
   pre='import json\nfrom tinydb import TinyDB,Query\nfrom tinydb.storages import MemoryStorage\ndb=TinyDB(storage=MemoryStorage)\nQ=Query()\n'
   r=subprocess.run(['python','-c',pre+code],cwd=temp,text=True,capture_output=True,check=True)
   row={'seed':seed,**json.loads(r.stdout)};results.append(row);print(json.dumps(row))
  finally:subprocess.run(['git','-C',str(ROOT),'worktree','remove','--force',temp],check=True,capture_output=True)
assert all(x['defect_confirmed'] for x in results)
(Path(__file__).parent/'behavioral-verification.json').write_text(json.dumps({'timing':'post-E2 reproducibility check','results':results},indent=2)+'\n')
