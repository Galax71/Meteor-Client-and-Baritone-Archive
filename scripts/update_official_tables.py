#!/usr/bin/env python3
"""Update README and DOWNLOADS tables from already-downloaded official JARs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
entries=[x for x in json.loads((root/'RECOVERED-SOURCES.json').read_text())['files'] if x['path'].startswith('source/meteorclient.com/')]
def key(x):
 v=x['path'].split('/')[4]
 return tuple(int(y) for y in v.split('.'))
entries.sort(key=key,reverse=True)
lines=['<!-- OFFICIAL_METEOR_START -->','## Official Meteor Client website downloads','',
       f'These **{len(entries)} JARs have been downloaded and committed** from [Meteor\'s official version archive](https://meteorclient.com/archive). See [RECOVERED-SOURCES.json](RECOVERED-SOURCES.json) for original URLs and SHA-256 hashes. In-game compatibility has not been verified.','']
for mod,title in [('meteor','Meteor Client'),('baritone','Baritone')]:
 lines.extend(['### '+title,'','| Minecraft version | Loader | Mod version / build | Download |','|---|---|---|---|'])
 for item in entries:
  p=item['path'].split('/')
  if p[2]!=mod:continue
  lines.append(f'| {p[4]} | {p[3]} | {p[5][:-4]} | [Download JAR]({item["path"]}) |')
 lines.append('')
lines.append('<!-- OFFICIAL_METEOR_END -->')
block='\n'.join(lines)
for name in ['README.md','DOWNLOADS.md']:
 p=root/name
 text=p.read_text()
 a=text.find('<!-- OFFICIAL_METEOR_START -->')
 b=text.find('<!-- OFFICIAL_METEOR_END -->')
 if a>=0 and b>a:text=text[:a]+block+text[b+len('<!-- OFFICIAL_METEOR_END -->'):]
 else:text=text.rstrip()+'\n\n'+block+'\n'
 p.write_text(text)
print('Updated official-site download tables:',len(entries),'JARs')
