#!/usr/bin/env python3
import os,json,re,hashlib,urllib.request,zipfile,io,pathlib,urllib.parse
root=pathlib.Path(__file__).resolve().parents[1]; base=root/'source'; records=[]; token=os.getenv('GITHUB_TOKEN','')
def fetch(url):
 h={'User-Agent':'archive-recovery/1.0'}
 if token and 'api.github.com' in url:h['Authorization']='Bearer '+token
 with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=60) as r:return r.read(75000001)
def save(url,source,mod,loader,mc,name,sha=None):
 if not re.fullmatch(r'(?:1\.\d+(?:\.\d+)?|26\.\d+(?:\.\d+)?)',mc):return
 if not re.fullmatch(r'[A-Za-z0-9._-]+\.jar',name):return
 try:
  data=fetch(url)
  if len(data)>75000000 or not zipfile.is_zipfile(io.BytesIO(data)):raise ValueError('invalid jar or too large')
  digest=hashlib.sha256(data).hexdigest()
  if sha and sha!=digest:raise ValueError('SHA256 mismatch')
  p=base/source/mod/loader/mc/name
  if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest:return
  if p.exists():p=p.with_name(p.stem+'_'+digest[:10]+'.jar')
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  records.append(dict(path=str(p.relative_to(root)),source_url=url,sha256=digest,bytes=len(data),tested_in_game=False))
  print('IMPORTED',p.relative_to(root),flush=True)
 except Exception as e:print('SKIPPED',name,str(e),flush=True)
for page in range(1,11):
 try: releases=json.loads(fetch('https://api.github.com/repos/cabaletta/baritone/releases?per_page=100&page='+str(page)))
 except Exception as e:print('Baritone API error',e);break
 if not releases:break
 for release in releases:
  line=next((x for x in (release.get('body') or '').splitlines() if 'minecraft' in x.lower()),'')
  mcvers=set(re.findall(r'(?<![\d.])(?:1\.\d{1,2}(?:\.\d{1,2})?|26\.\d+(?:\.\d+)?)(?![\d.])',line))
  for a in release.get('assets',[]):
   name=a.get('name','')
   if not name.endswith('.jar'):continue
   loader='neoforge' if 'neoforge' in name else 'fabric' if 'fabric' in name else 'forge' if 'forge' in name else 'standalone'
   digest=a.get('digest') or '';digest=digest[7:] if digest.startswith('sha256:') else None
   for mc in mcvers:save(a['browser_download_url'],'github.com-cabaletta-baritone','baritone',loader,mc,name,digest)
known={'0.3.0.1':'1.16.1','0.4.6':'1.17.1','0.4.7':'1.18.1','0.4.8':'1.18.2','0.5.0':'1.19','0.5.1':'1.19.2','0.5.5':'1.20.2','0.5.6':'1.20.4','0.5.7':'1.20.6','0.5.8':'1.21.1'}
try:
 tree=json.loads(fetch('https://api.github.com/repos/ManInMyVan/meteor-archive/git/trees/main?recursive=1'))['tree']
 for item in tree:
  path=item.get('path','');name=path.split('/')[-1]
  if not path.startswith('files/') or not name.endswith('.jar'):continue
  if '/meteor-client/' in path:
   match=re.search(r'meteor-client-(0\.\d+(?:\.\d+){1,2})',name)
   if not match or match.group(1) not in known:continue
   mc=known[match.group(1)];mod='meteor'
  elif '/baritone/' in path:
   match=re.search(r'baritone-(1\.\d+(?:\.\d+)?)',name)
   if not match:continue
   mc=match.group(1);mod='baritone'
  else:continue
  save('https://raw.githubusercontent.com/ManInMyVan/meteor-archive/main/'+urllib.parse.quote(path,safe='/'),'github.com-ManInMyVan-meteor-archive',mod,'fabric',mc,name)
except Exception as e:print('Community archive error',e)

# Import non-GitHub direct downloads listed in a reviewed source manifest.
external=root/'EXTERNAL-DOWNLOADS.json'
if external.exists():
 try:
  for item in json.loads(external.read_text()).get('downloads',[]):
   url=item['url'];host=urllib.parse.urlparse(url).hostname or ''
   if urllib.parse.urlparse(url).scheme!='https' or not host:continue
   if host in ('localhost','127.0.0.1') or host.endswith('.local'):continue
   source=re.sub(r'[^a-zA-Z0-9._-]','-',host)
   save(url,source,item['mod'],item['loader'],item['minecraft_version'],item['filename'],item.get('sha256'))
 except Exception as e:print('External source manifest error',e)

manifest=root/'RECOVERED-SOURCES.json'
prior=json.loads(manifest.read_text())['files'] if manifest.exists() else []
items={x['path']:x for x in prior}
for r in records:items[r['path']]=r
manifest.write_text(json.dumps({'files':sorted(items.values(),key=lambda x:x['path'])},indent=2)+'\n')
print('New files:',len(records))
