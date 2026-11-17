#!/usr/bin/env python3
"""Cerca lezioni/registrazioni in Notion locale e Voice Memos. macOS."""
import argparse, json, re, sqlite3, subprocess
from pathlib import Path

NOTION = Path.home()/"Library/Application Support/Notion/notion.db"

def notion_titles(q, limit=8):
    if not NOTION.exists(): return []
    try:
        con=sqlite3.connect(f'file:{NOTION}?mode=ro', uri=True)
        rows=con.execute("select properties from block where alive=1 and type='page' and properties like ? limit ?",(f'%{q}%',limit*3)).fetchall()
        con.close()
    except Exception as e:
        return [f'ERR Notion: {e}']
    out=[]
    for (prop,) in rows:
        try:
            d=json.loads(prop or '{}')
            title=''.join(seg[0] for seg in d.get('title',[]) if seg)
        except Exception:
            title=re.sub(r'<[^>]+>',' ',prop or '')[:120]
        title=title.strip().replace('\n',' ')
        if title and title not in out:
            out.append(title)
    return out[:limit]

def audio_files():
    roots=[Path.home()/"Library/Group Containers/group.com.apple.VoiceMemos.shared",
           Path.home()/"Library/Containers/com.apple.VoiceMemos"]
    out=[]
    for root in roots:
        try:
            for p in root.rglob('*'):
                if p.suffix.lower() in ('.m4a','.qta','.caf','.wav','.mp3'):
                    out.append(p)
        except Exception:
            pass
    # Spotlight fallback
    try:
        r=subprocess.run(['mdfind','kMDItemFSName == "*.m4a"'],capture_output=True,text=True,timeout=15)
        for line in r.stdout.splitlines():
            p=Path(line)
            if any(x in str(p).lower() for x in ('voicememo','memo','registrazioni')):
                out.append(p)
    except Exception:
        pass
    return sorted(set(out))

def transcribe(files, outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    model=Path.home()/'.jarvis/models/ggml-small.bin'
    if not model.exists():
        print('Whisper model non trovato:',model); return
    for f in files:
        dst=outdir/(f.stem+'.txt')
        print('Trascrivo',f)
        subprocess.run(['whisper-cli','-m',str(model),'-f',str(f),'-l','it','-otxt','-of',str(dst.with_suffix(''))],check=False)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--query',required=True)
    ap.add_argument('--limit',type=int,default=8)
    ap.add_argument('--transcribe',action='store_true')
    ap.add_argument('--out',default=str(Path.home()/'Documents/Scuola/Registrazioni'))
    a=ap.parse_args()
    print('## Notion')
    for t in notion_titles(a.query,a.limit): print('-',t)
    files=audio_files()
    print('## File audio')
    if not files: print('- nessun file accessibile (Voice Memos può essere protetto da macOS)')
    for f in files[:a.limit]: print('-',f)
    if a.transcribe and files:
        transcribe(files,Path(a.out)/a.query)
        print('## Trascrizioni in',Path(a.out)/a.query)

if __name__=='__main__': main()
