from decimal import Decimal
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent
path=ROOT/'public/study.json'
study=json.loads(path.read_text(encoding='utf-8'));pairs=study['pairs']
timestamps=[row['timestamp'] for row in pairs]
assert timestamps==sorted(set(timestamps)), 'Timestamps must be unique and chronological'
threshold=Decimal(str(study['threshold']));edges=[]
for row in pairs:
 assert row['polymarketYes']['timestamp']==row['timestamp']==row['kalshiNo']['timestamp']
 edge=(Decimal('1')-Decimal(str(row['polymarketYes']['close']))-Decimal(str(row['kalshiNo']['close']))).quantize(Decimal('0.00000001'))
 assert edge==Decimal(str(row['edge'])), 'Stored spread does not match the two closes'
 edges.append(edge)
print('Predictefy arbitrage research | Python')
print('Dataset: Republican House control, 2026')
print('Matching hourly observations:',len(pairs))
split=study['split']
for label,values in [('development',edges[:split]),('holdout',edges[split:])]:
 passing=sum(value>threshold for value in values)
 assert len(values)==study[label]['rows']
 assert passing==study[label]['above1pct'], 'Recomputed count differs from stored summary'
 print(f'{label}: {len(values)} observations | {passing} spreads strictly above 1 cent')
print('Executable fills: not established by hourly candles')
print('Dataset SHA256:',hashlib.sha256(path.read_bytes()).hexdigest()[:20])
