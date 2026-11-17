#!/usr/bin/env python3
"""Estrae 5 domande flash da una cartella di studio (Markdown + Canvas)."""
import json, random, re, sys
from pathlib import Path

def texts_from_folder(root: Path):
    out=[]
    for p in sorted(root.rglob('*')):
        if p.suffix.lower()=='.md':
            out += p.read_text(errors='ignore').splitlines()
        elif p.suffix.lower()=='.canvas':
            try: d=json.loads(p.read_text())
            except Exception: continue
            for n in d.get('nodes',[]):
                if n.get('type')=='text':
                    out += n.get('text','').splitlines()
    return [x.strip(' *\t-') for x in out if x.strip()]

def main():
    if len(sys.argv)<2:
        print('Uso: flash_quiz.py <cartella> [n]'); raise SystemExit(1)
    root=Path(sys.argv[1]).expanduser(); n=int(sys.argv[2]) if len(sys.argv)>2 else 5
    lines=texts_from_folder(root)
    qs=[]
    for x in lines:
        if 18 <= len(x) <= 220 and x.endswith('?'):
            qs.append(x)
    # fallback: usa i titoli dei nodi come "Spiega ..."
    if len(qs)<n:
        labels=[]
        for x in lines:
            if 3 <= len(x) <= 70 and not x.startswith('http') and not x.endswith('?'):
                labels.append(x)
        random.Random(7).shuffle(labels)
        for x in labels:
            q=f"Spiega: {x}"
            if q not in qs: qs.append(q)
            if len(qs)>=n: break
    for i,q in enumerate(qs[:n],1): print(f'{i}. {q}')

if __name__=='__main__': main()
