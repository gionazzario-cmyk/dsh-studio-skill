#!/usr/bin/env python3
"""Crea la struttura minima di una materia in Obsidian e su SSD."""
import argparse, json, uuid
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('materia')
    ap.add_argument('--vault', default=str(Path.home()/'Documents/Obsidian Vault'))
    ap.add_argument('--ssd', default=str(Path.home()/'Documents/Scuola'))
    a=ap.parse_args()
    vault=Path(a.vault)/a.materia; vault.mkdir(parents=True,exist_ok=True)
    ssd=Path(a.ssd)/a.materia
    for sub in ['ClasseViva','Classroom','Libro','OCR','Registrazioni','Spiegati bene','Piano_Giornaliero']:
        (ssd/sub).mkdir(parents=True,exist_ok=True)
    ctx=vault/'00_Contesto.md'
    if not ctx.exists():
        ctx.write_text(f'''# {a.materia} — contesto rapido

## Libri
- da compilare (BooktabZ / HUB Young / My Digital Book)

## Date
- ultima verifica:
- prossima scadenza:

## Materiali
- SSD: `{ssd}`
- Obsidian: `{vault}`

## Regola low-token
Prima leggi questo file, poi riusa mappe, OCR e video esistenti.
''')
    idx=vault/'00_Indice.canvas'
    if not idx.exists():
        root=str(uuid.uuid4())[:12]
        nodes=[{"id":root,"type":"text","text":f"# {a.materia}\nIndice di studio","x":-180,"y":-60,"width":360,"height":100,"color":"1"}]
        idx.write_text(json.dumps({"nodes":nodes,"edges":[]},ensure_ascii=False,indent=2))
    print(vault); print(ssd)

if __name__=='__main__': main()
