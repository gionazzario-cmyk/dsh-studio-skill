#!/usr/bin/env python3
"""Create one text-only Obsidian Canvas in CmapTools style.

Usage: python3 make_canvas.py spec.json
Spec: {out, title, sub, kicker, num, source, branches:[{label,text,color,slot}]}
No images by design.
"""
import json, sys, uuid
from pathlib import Path

def nid(): return str(uuid.uuid4())[:12]

def text_node(text, x, y, w, h, color=None):
    d = {"id": nid(), "type": "text", "text": text, "x": x, "y": y, "width": w, "height": h}
    if color: d["color"] = str(color)
    return d

def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    nodes = [
        {"id": "bg", "type": "group", "x": 0, "y": 0, "width": 1600, "height": 900,
         "label": "", "background": "#14181F", "backgroundStyle": "solid"},
        {"id": "strip", "type": "group", "x": 0, "y": 0, "width": 16, "height": 900,
         "label": "", "background": "#8C1D2F", "backgroundStyle": "solid"},
        text_node(f"**{spec.get('kicker','STUDIO')}**", 60, 30, 700, 30),
        text_node(f"**{int(spec.get('num',1)):02d}**", 1480, 30, 60, 30),
    ]
    center = text_node(f"# {spec['title']}\n{spec.get('sub','')}", 620, 320, 360, 190, "1")
    nodes.append(center)
    slots = {
        "left-top": (60, 100, 480, 190, "left"),
        "left-bottom": (60, 530, 480, 170, "left"),
        "right-top": (1060, 100, 480, 190, "right"),
        "right-bottom": (1060, 530, 480, 170, "right"),
        "bottom": (620, 730, 360, 140, "bottom"),
    }
    order = ["left-top", "right-top", "left-bottom", "right-bottom", "bottom"]
    edges = []
    for i, b in enumerate(spec.get("branches", [])):
        slot = b.get("slot") or order[i % len(order)]
        x, y, w, h, side = slots.get(slot, slots[order[i % len(order)]])
        node = text_node(f"**{b['label']}**\n{b['text']}", x, y, w, h, b.get("color", "5"))
        nodes.append(node)
        edges.append({"id": nid(), "fromNode": center["id"], "fromSide": side,
                      "toNode": node["id"], "toSide": "left" if side in ("left", "right") else "top"})
    nodes.append(text_node(f"*{spec.get('source','')}*", 620, 790, 360, 50))
    out = Path(spec["out"]).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2))
    print(out)

if __name__ == "__main__":
    main()
