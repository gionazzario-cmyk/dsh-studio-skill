#!/usr/bin/env python3
"""Cattura N pagine visibili di un'app libro e le OCRizza. macOS only."""
import argparse, subprocess, time
from pathlib import Path
from PIL import Image

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--app', default='BooktabZ')
    ap.add_argument('--pages', type=int, default=1)
    ap.add_argument('--out', required=True)
    ap.add_argument('--crop', default='', help='x,y,w,h in pixel')
    ap.add_argument('--key', type=int, default=124, help='key code: 124 right, 123 left')
    ap.add_argument('--delay', type=float, default=1.2)
    a=ap.parse_args()
    out=Path(a.out).expanduser(); out.mkdir(parents=True, exist_ok=True)
    subprocess.run(['osascript','-e',f'tell application "{a.app}" to activate'],check=True)
    time.sleep(1.0)
    for i in range(a.pages):
        png=out/f'page_{i+1:03d}.png'; txt=out/f'page_{i+1:03d}.txt'
        subprocess.run(['screencapture','-x',str(png)],check=True)
        if a.crop:
            x,y,w,h=[int(v) for v in a.crop.split(',')]
            im=Image.open(png); im.crop((x,y,x+w,y+h)).save(png)
        ocr_bin = Path(__file__).with_name('ocr')
        if not ocr_bin.exists():
            subprocess.run(['swiftc','-O',str(Path(__file__).with_name('ocr.swift')),'-o',str(ocr_bin)],check=True)
        subprocess.run([str(ocr_bin),str(png)],check=True,stdout=txt.open('w'))
        print(png, txt)
        if i<a.pages-1:
            subprocess.run(['osascript','-e',f'tell application "System Events" to key code {a.key}'],check=True)
            time.sleep(a.delay)

if __name__=='__main__': main()
