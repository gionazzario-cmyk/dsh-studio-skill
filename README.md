# DSH Studio Skill

Skill per **DeepSeek Harness**: `/studio <materia> <uso> <argomento>`.

Trasforma una richiesta di studio in un workflow completo:

- legge `00_Contesto.md` della materia (low-token);
- cerca lezioni e compiti su ClasseViva e Google Classroom;
- usa i libri digitali e, se sono protetti, cattura le pagine con screenshot + OCR locale;
- cerca lezioni registrate in Notion e nei memo vocali, con trascrizione Whisper locale;
- crea mappe e slide Obsidian Canvas;
- produce una mini-lezione video 9:16 ADHD-friendly;
- chiude con un report fisso.

## Installazione

```bash
mkdir -p ~/.dsh/skills
git clone https://github.com/gionazzario-cmyk/dsh-studio-skill.git ~/.dsh/skills/studio
chmod +x ~/.dsh/skills/studio/scripts/*.sh ~/.dsh/skills/studio/scripts/*.py
swiftc -O ~/.dsh/skills/studio/scripts/ocr.swift -o ~/.dsh/skills/studio/scripts/ocr
```

Requisiti macOS: Python 3 con Pillow, `screencapture`, `swiftc`, `ffmpeg`, `edge-tts`; opzionali `whisper-cli` e modello Whisper.

## Uso

```text
/studio Arte spiegami Ravenna
/studio Fisica farmi una mappa sul moto accelerato
/studio Arte ripasso flash su San Vitale
```

## Struttura

- `SKILL.md` — istruzioni della skill
- `scripts/make_canvas.py` — genera canvas Obsidian
- `scripts/studio_init.py` — crea cartelle, contesto e indice
- `scripts/flash_quiz.py` — 5 domande di ripasso
- `scripts/find_recordings.py` — cerca Notion e memo vocali, trascrive
- `scripts/capture_book.py` — cattura pagine e OCR
- `scripts/ocr.swift`, `ocr_image.sh` — OCR locale Vision
- `templates/video_adhd.md` — struttura video

## Note

Nessuna credenziale o dato personale è incluso. Le password e i codici libro restano locali.
