---
name: studio
description: "Studio assistito per qualsiasi materia e uso: /studio <materia> <uso> <argomento>. Estrae lezioni e compiti, usa i libri, crea mappe Obsidian, slide “Spiegati bene” e video."
user-invocable: true
---

# /studio

Quando l'utente scrive `/studio <materia> <richiesta>`, esegui questo workflow. Se manca la materia o la richiesta, chiedi solo quello che manca in una riga.

## 0. Regole
- Non inviare messaggi a compagni, professori o terzi senza conferma esplicita.
- Non cancellare file senza aver verificato il percorso assoluto e la copia di backup.
- Preferisci strumenti locali (Vision, Ollama, ffmpeg, Edge TTS). Usa API a pagamento solo con ok esplicito.
- Se serve una password o un codice libro, chiedilo e fermati: non inventare credenziali.
- Dichiara sempre cosa hai verificato e cosa non hai potuto verificare.

## 0b. Low-token (default)
Prima di tutto cerca `<Materia>/00_Contesto.md` (Obsidian o SSD) e leggilo: contiene libri, date, lezioni e percorsi.
Poi:
- riusa mappe, canvas, slide, OCR e video già presenti;
- non rileggere ClasseViva/Classroom/libro se il contesto è aggiornato;
- non rigenerare un video intero se basta correggere l’audio o una scena; riusa il video esistente se l’argomento è lo stesso;
- fai poche operazioni mirate e chiudi con un report di massimo 10 righe;
- se manca solo un dato, chiedilo in una riga e fermati.

## 0c. File protetti (BooktabZ / HUB Young)
- **Non chiedere all’utente di esportare o fare screenshot**: se il libro è visibile, cattura tu la pagina.
- Se il testo è protetto/DRM ma leggibile a schermo, usa screenshot + OCR locale; non forzare l’estrazione dal file.
- Chiedi qualcosa solo se lo schermo è nero/DRM impedisce la visualizzazione o serve una password.

## 0d. Screenshot + OCR automatici
Strumenti già pronti in `scripts/`:
```bash
# una pagina
screencapture -x /tmp/pagina.png
~/.dsh/skills/studio/scripts/ocr_image.sh /tmp/pagina.png

# N pagine, cambiando pagina con la freccia destra
python3 ~/.dsh/skills/studio/scripts/capture_book.py \
  --app BooktabZ --pages 5 --out "<Materia>/Libro/screenshots" \
  --crop "400,150,1150,850"
```
Poi:
- salva screenshot in `<Materia>/Libro/screenshots/` e testi in `<Materia>/OCR/`;
- se l’OCR è illeggibile: aumenta lo zoom, passa alla vista pagina singola, ritaglia più stretto e riprova;
- non fermarti a chiedere all’utente: fai tu 2-3 tentativi mirati.

## 1. Capisci la richiesta
Estrai:
- **materia** (es. Arte, Fisica, Latino);
- **compito** (studiare un blocco, preparare una verifica, fare una mappa, un video, recuperare un voto);
- **scadenza** e **classe** se presenti.

## 1b. Uso richiesto
Riconosci l’uso e adatta il risultato:
- **spiegami / lezione** → canvas di sintesi + **video lezione** (sempre, max 10 min);
- **schema / mappa** → canvas;
- **spiegati bene** → un canvas per argomento, senza immagini;
- **schema per giorno** → piano giornaliero;
- **esercizi** → esercizi + soluzioni;
- **verifica / simulazione** → domande + risposte;
- **riassunto** → sintesi breve;
- **recupero** → priorità + piano mirato;
- **video** → video lezione 9:16, max 10 min;
- **ripasso flash** → 5 domande trabocchetto dalle mappe/lezioni, senza rispiegare tutto.

## 2. Raccolta dati
1. **ClasseViva** (`web.spaggiari.eu`, account famiglia): filtra per materia in *Valutazioni*, *Lezioni*, *Materiali/Compiti*, *Agenda*.
2. **Google Classroom** (account scuola `<account scuola>`): corso, *Lavori del corso*, materiali, PDF/slide.
3. **Libri**: controlla BooktabZ / HUB Young / My Digital Book. In BooktabZ l'account scuola è già attivo; se il volume non c'è, chiedi il codice di attivazione.
4. **Fonti locali**: Obsidian Vault, CmapTools, appunti, chat, screenshot. Cerca per materia e per parole chiave.
5. **SSD**: `/Volumes/<SSD>/scuola/<anno>/<quadrimestre>/<Materia>/`.
6. **Registrazioni**: cerca su Notion e nei memo vocali prima di dire che una lezione manca:
```bash
python3 ~/.dsh/skills/studio/scripts/find_recordings.py --query "<materia o argomento>" --limit 8
```
Se serve, aggiungi `--transcribe`: usa `whisper-cli` locale e salva in `<Materia>/Registrazioni/`.

## 3. Salvataggio
- Per la struttura minima usa `scripts/studio_init.py <Materia> --vault ... --ssd ...`: crea cartelle, `00_Contesto.md` e `00_Indice.canvas`.
- Crea una cartella materia con sottocartelle `ClasseViva/`, `Classroom/`, `Libro/`, `OCR/`, `Registrazioni/`, `Spiegati bene/`, `Piano_Giornaliero/` (solo se servono).
- Copia i materiali sull'SSD, non lasciare doppioni sul Mac.
- Verifica con `find`, `du`, `shasum`; scrivi un `MANIFEST_SHA256.txt`.

## 4. Elaborazione
- OCR locale delle immagini con Vision di macOS.
- Sintesi con Ollama (`qwen3:30b-a3b` o modello adatto) solo sui testi necessari.
- Per il libro: usa indice, unità e pagine; non inventare ciò che non è nel volume.
- Incrocia sempre libro + lezione + materiali Classroom.

## 4b. Registrazioni delle lezioni
- Prima di dire “non ho la lezione”, cerca in **Notion** e nei **memo vocali** con `find_recordings.py`.
- Se trovi un audio, trascrivilo in locale con `whisper-cli` (modello `~/.jarvis/models/ggml-small.bin`), non con API.
- Salva trascrizione e audio in `<Materia>/Registrazioni/` e usa la trascrizione come fonte.
- Se Voice Memos è protetto da macOS, usa l’app o i file `memo-*.m4a` accessibili; non chiedere all’utente di caricare file.

## 5. Mappe e “Spiegati bene”
- Crea/aggiorna `~/Documents/Obsidian Vault/<Materia>/`.
- Le slide richieste vanno in `<Materia>/Spiegati bene/`, **un canvas per argomento, senza immagini**, in stile CmapTools: nodo centrale, rami, fonte.
- Adatta i rami alla materia, non usare per forza lo schema dell’Arte:
  - **Arte/Storia**: contesto · opere/eventi · linguaggio · confronti · cosa dire.
  - **Fisica/Matematica**: definizioni · formule/teoremi · procedimento · esercizi · errori.
  - **Latino/Greco**: regole · paradigmi · eccezioni · traduzione · esercizi.
  - **Lingue**: funzioni · grammatica · lessico · esempi · errori.
  - **Scienze**: fenomeni · modelli · processi · dati · collegamenti.
- Colori: 1 centro, 5 contesto, 3 struttura/opere, 4 concetti, 6 sintesi.
- Per risparmiare token usa `scripts/make_canvas.py` con un JSON minimale, invece di riscrivere il codice del canvas.
- Aggiorna `00_Indice.canvas` e `00_Contesto.md`.
- Non rifare solo le mappe nuove: se richiesto “tutte”, rigenera anche le esistenti.
- Se l’utente chiede “senza immagini”, non inserire file node: solo testo e archi.


Esempio di specifica per `make_canvas.py`:
```json
{"out":".../<Materia>/Spiegati bene/01_Tema.canvas","title":"Tema","sub":"Materia · unità","kicker":"MATERIA","num":1,"source":"Libro, pp. ...",
 "branches":[
  {"label":"DEFINIZIONE","text":"- ...","color":"5","slot":"left-top"},
  {"label":"FORMULA","text":"- ...","color":"3","slot":"right-top"},
  {"label":"ESEMPIO","text":"- ...","color":"4","slot":"left-bottom"},
  {"label":"ERRORI","text":"- ...","color":"6","slot":"right-bottom"}]}
```

## 5c. Ripasso flash
Se l'utente chiede **ripasso flash**, esegui:

```bash
python3 ~/.dsh/skills/studio/scripts/flash_quiz.py "<Materia>" 5
```

Poi:
- fai le 5 domande una alla volta, senza mostrare le risposte;
- attendi la risposta dell'utente;
- dai un voto sintetico (0-2 per domanda) e indica la mappa da rileggere;
- non rispiegare tutto: solo i punti sbagliati.

## 5b. Schema per giorno
Se l'utente chiede uno **schema per giorno**:
- crea `<Materia>/Piano_Giornaliero/` con un file per ogni giorno (`Giorno_1.md`, ...);
- crea anche `00_Piano_7_giorni.canvas` con una colonna per giorno;
- ogni giorno contiene: 5 min ripasso del giorno prima, 20 min argomento nuovo, 10 min recall a voce, 10 min tavola/esercizio, 3 domande di controllo e una checkbox;
- indica sempre pagine del libro e mappa da usare;
- chiudi con una simulazione e un ripasso generale.

## 6. Video lezione ADHD-friendly (sempre)
L’utente ha **ADHD**: ogni spiegazione/studio produce anche un video che deve **spiegare bene** e **attirare l’attenzione**. Leggi `templates/video_adhd.md` e seguilo.
Durata **5-10 minuti** (target 6-8), un argomento per video. Non fare clip da 60 secondi: spiega, non elencare.
- Struttura: hook 10-15 s → roadmap → 3-5 blocchi spiegati (cos’è/perché/esempio) → confronto → recap in 3 punti.
- 1080×1920, 30 fps, H.264 + AAC.
- Text-only o con immagini già presenti; cambi visivi ogni 5-8 s, max 8 parole per card, sottotitoli grandi.
- Voce: Gemini TTS se disponibile; altrimenti Edge TTS `it-IT-ElsaNeural`. Mai la voce macOS Alice.
- Musica soft generata in locale, volume basso.
- Salva `VIDEO_<ARGOMENTO>_9x16.mp4` e `SCENEGGIATURA_<ARGOMENTO>.md` nella cartella della materia; aggiungi una checklist ADHD allo script (max 10 min).
- Se esiste già un video per lo stesso argomento, riusalo; rigenera solo se il contenuto è cambiato.

## 7. Report (formato fisso, max 8 righe)
Chiudi sempre con questo blocco:

```markdown
### 📊 Report Studio
- **📁 Salvato in:** [percorso SSD + Obsidian]
- **🛠️ Strumenti usati:** [OCR locale / Canvas / video / libro]
- **⏱️ Tempo stimato di ripasso:** [es. 25 min]
- **🎯 Prossimo step:** [es. ripasso flash su San Vitale]
```

Se qualcosa manca, aggiungi una sola riga `⚠️ Manca:` e fermati.

## 8. Economia
- Usa una sola passata di OCR e una sola sintesi locale.
- Non rigenerare video interi se basta correggere l'audio.
- Se una quota API è esaurita, dichiaralo e usa il fallback locale.
