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


# Keep the main README tables synchronized with the official recovered JARs.
readme=root/'README.md'
text=readme.read_text()
begin=text.index('## Downloads by mod')
end=text.index('## Minecraft Java releases',begin)
section=text[begin:end]
for mod,heading,next_heading in [('meteor','### Meteor Client','### Baritone'),('baritone','### Baritone',None)]:
 start=section.index(heading)
 finish=section.index(next_heading,start+len(heading)) if next_heading else len(section)
 chunk=section[start:finish]
 rows=chunk.splitlines()
 header=next(i for i,line in enumerate(rows) if line.startswith('| Minecraft version |'))
 stop=next((i for i in range(header+2,len(rows)) if not rows[i].startswith('|')),len(rows))
 previous=[line for line in rows[header+2:stop] if 'source/meteorclient.com/' not in line]
 recovered=[]
 for item in entries:
  p=item['path'].split('/')
  if p[2]!=mod:continue
  recovered.append(f'| {p[4]} | {p[3]} | {p[5][:-4]} (official archive filename) | [meteorclient.com](https://meteorclient.com/archive) | [Download JAR]({item["path"]}) |')
 def sortkey(line):
  v=line.split('|')[1].strip().split(' ')[0]
  return tuple(int(n) for n in v.split('.') if n.isdigit())
 combined=sorted(previous+recovered,key=sortkey,reverse=True)
 rows[header+2:stop]=combined
 section=section[:start]+'\n'.join(rows)+section[finish:]
text=text[:begin]+section+text[end:]
readme.write_text(text)

# Add explicit Missing rows for Minecraft versions without a local archive entry.
coverage=json.loads((root/'MC-VERSION-COVERAGE.json').read_text())
versions=list(dict.fromkeys(item['minecraft_version'] for item in coverage['records']))
readme=root/'README.md'
text=readme.read_text()
a=text.index('## Downloads by mod')
b=text.index('## Minecraft Java releases',a)
section=text[a:b]
for heading,next_heading in [('### Meteor Client','### Baritone'),('### Baritone',None)]:
 start=section.index(heading)
 stop=section.index(next_heading,start+len(heading)) if next_heading else len(section)
 chunk=section[start:stop]
 lines=chunk.splitlines()
 header=next(i for i,line in enumerate(lines) if line.startswith('| Minecraft version |'))
 existing=[line for line in lines[header+2:] if line.startswith('|') and not line.startswith('|---') and '**Missing**' not in line]
 present={line.split('|')[1].strip().replace(' (inferred)','') for line in existing}
 missing=[f'| {v} | — | **Missing** | — | **Missing** |' for v in versions if v not in present]
 def version_key(line):
  v=line.split('|')[1].strip().replace(' (inferred)','')
  return tuple(int(part) for part in v.split('.') if part.isdigit())
 rows=sorted(existing+missing,key=version_key,reverse=True)
 section=section[:start]+'\n'.join(lines[:header+2]+rows+[''])+'\n'+section[stop:]
text=text[:a]+section+text[b:]
readme.write_text(text)

# NOTE: The main README includes a Mod existed? column and early Minecraft milestones.
# Preserve this column when regenerating rows; historical evidence is maintained in MOD-EXISTENCE-NOTES.json.
