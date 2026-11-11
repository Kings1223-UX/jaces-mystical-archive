#!/usr/bin/env python3
"""Fetch Scryfall Oracle Cards bulk data and publish compact static JSON."""
import gzip, io, json, os, pathlib, urllib.request, datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'public'
OUT.mkdir(exist_ok=True)
API='https://api.scryfall.com/bulk-data/oracle-cards'
HEAD={'User-Agent':'JacesMysticalArchive/1.2 (personal playtest proxy website)','Accept':'application/json'}
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=120)
with get(API) as response:
    meta = json.load(response)
# Support a response wrapped in a "data" object.
if isinstance(meta, dict) and isinstance(meta.get("data"), dict):
    meta = meta["data"]
if not isinstance(meta, dict):
    raise RuntimeError(
        "Unexpected Scryfall response format."
    )
if "download_uri" not in meta:
    raise RuntimeError(
        "Scryfall did not provide a download_uri. "
        f"Response: {json.dumps(meta)[:1500]}"
    )
version = meta.get("updated_at", "unknown")
oldfile=OUT/'database-version.json'
if oldfile.exists():
 try:
  old=json.loads(oldfile.read_text())
  if old.get('updated_at')==version and (OUT/'cards.json').exists():
   print('Database unchanged:',version);raise SystemExit(0)
 except (ValueError,KeyError):pass
url=meta['download_uri']
print('Downloading Oracle Cards:',version,flush=True)
fields=('name','type_line','oracle_text','mana_cost','power','toughness','colors')
cards=[]
with get(url) as response:
 stream=gzip.GzipFile(fileobj=response) if url.split('?')[0].endswith('.gz') or response.headers.get('Content-Encoding')=='gzip' else response
 # Scryfall may provide JSONL or a JSON array depending on the export.
 first=stream.read(1)
 while first in (b' ',b'\n',b'\r',b'\t'):first=stream.read(1)
 def compact(card):
  out={k:card[k] for k in fields if k in card}
  if card.get('card_faces'):
   out['card_faces']=[{k:face[k] for k in fields if k in face} for face in card['card_faces']]
  return out
 if first==b'[':
  # JSON array bulk exports; streaming JSON parser via optional ijson when available.
  try:import ijson
  except ImportError:raise RuntimeError('JSON array detected. Install ijson in CI to stream this export.')
  class Prefix(io.RawIOBase):
   def __init__(self,prefix,base):self.prefix=prefix;self.base=base
   def readable(self):return True
   def readinto(self,b):
    if self.prefix:
     b[0]=self.prefix[0];self.prefix=self.prefix[1:];return 1
    chunk=self.base.read(len(b));b[:len(chunk)]=chunk;return len(chunk)
  for card in ijson.items(io.BufferedReader(Prefix(first,stream)),'item'):
   if card.get('name'):cards.append(compact(card))
 else:
  for line in io.TextIOWrapper(stream,encoding='utf-8'):
   if not line.strip():continue
   card=json.loads((first.decode('utf-8')+line) if first else line)
   first=b''
   if card.get('name'):cards.append(compact(card))
if len(cards)<1000:raise RuntimeError(f'Unexpectedly small database: {len(cards)} cards')
print('Validated',len(cards),'cards',flush=True)
tmp=OUT/'cards.json.tmp'
with tmp.open('w',encoding='utf-8') as f:json.dump(cards,f,ensure_ascii=False,separators=(',',':'))
tmp.replace(OUT/'cards.json')
oldfile.write_text(json.dumps({'updated_at':version,'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(cards),'source':API},indent=2)+'\n')
print('Published',len(cards),'cards; size',round((OUT/'cards.json').stat().st_size/1e6,1),'MB')
