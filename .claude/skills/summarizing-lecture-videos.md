---
name: summarizing-lecture-videos
description: Use when Praneel shares a recorded lecture (Canvas page link, MP4 file, video URL) and wants real understanding, not a skim — argumentation, examples, testable claims, structure of the argument. Triggers: "I don't want to listen to this whole lecture," "summarize but make me actually learn it," "give me your judgement to teach me," "what's the argumentation and examples."
---

# Summarizing lecture videos

When Praneel shares a recorded lecture — Canvas link, MP4 file, video URL — and asks for a summary that *teaches* him, the work is not "extract bullet points." It is: download the video locally, transcribe it on the GPU, and synthesize a deep summary that surfaces the argumentation, examples, and likely-testable claims as if he had attended. Skipping the transcription step (e.g., guessing content from the course title) is the failure mode. Take agency — the tools to do this end-to-end are local.

## When to use

- Praneel shares a Canvas course video URL or any recorded lecture link/file
- He says some version of "I don't want to listen to this," "summarize but teach me," "what are the arguments / examples," "use your judgement to teach me"
- Academic, educational, or structured-talk content where *how the argument is built* matters, not just topics

## When not to use

- He wants a quick skim or topic list — give that without the full pipeline
- The page already has reliable captions/transcript — read those instead of re-transcribing
- It's a podcast or unstructured conversation (this skill targets structured argument)

## Step 1 — get the video

**Canvas** (`*.instructure.com`): pages embed video via `iframe[src*="media_attachments_iframe"]`. Pull the file ID from the iframe src, then GET `https://<host>/api/v1/files/<id>` to get JSON metadata including the direct download URL (`https://<host>/files/<id>/download?download_frd=1`). That URL respects auth cookies — trigger it from Chrome MCP via JS:

```js
const a = document.createElement('a');
a.href = 'https://<host>/files/<id>/download?download_frd=1';
a.download = '<name>.mp4';
document.body.appendChild(a); a.click(); a.remove();
```

The Canvas media-attachments API may report the file size as wrong (placeholder bytes); the actual download is the real video. Trust the download, not the metadata `size`.

If the page uses a custom JS player, the `<video>` element may not exist in the DOM until play is clicked. Skip the player entirely and go to the Canvas files API path above.

**Other platforms**: inspect the DOM for direct `<source src="...mp4">`, check network requests after clicking play for `.mp4` / `.m3u8`. For HLS-only streams, `yt-dlp` or `ffmpeg -i <manifest.m3u8> -c copy out.mp4`.

Drop the file in `C:\Users\prapa\Downloads\` (per the output-file-location memory — Praneel wants generated artifacts in Downloads, not the home dir).

## Step 2 — transcribe locally with GPU

`faster-whisper` with `large-v3` on GPU is the gold standard for academic content with proper nouns. The script that handles all the Windows gotchas:

```python
import sys, time, os, site
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# Windows: register CUDA DLLs from pip nvidia packages BEFORE importing CTranslate2
for sp in site.getsitepackages() + [site.getusersitepackages()]:
    for sub in ("nvidia/cublas/bin", "nvidia/cudnn/bin"):
        p = os.path.join(sp, sub)
        if os.path.isdir(p):
            os.add_dll_directory(p)
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
from huggingface_hub import snapshot_download
from faster_whisper import WhisperModel

SRC = r"C:\Users\prapa\Downloads\<file>.mp4"
OUT_TXT = r"C:\Users\prapa\Downloads\<name>_transcript.txt"
OUT_TIMED = r"C:\Users\prapa\Downloads\<name>_timed.txt"

# Bypass HF symlink cache (Windows perms) by downloading model to a local dir
local = snapshot_download(
    repo_id="Systran/faster-whisper-large-v3",
    local_dir=r"C:\Users\prapa\models\faster-whisper-large-v3",
)
model = WhisperModel(local, device="cuda", compute_type="float16")
# Fallback if GPU/CUDA unavailable: WhisperModel("small.en", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    SRC, beam_size=5, vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
    language="en", condition_on_previous_text=True,
)
print(f"duration={info.duration/60:.1f}min", flush=True)

plain, timed = [], []
last = time.time()
for seg in segments:
    plain.append(seg.text.strip())
    mm, ss = int(seg.start // 60), int(seg.start % 60)
    timed.append(f"[{mm:02d}:{ss:02d}] {seg.text.strip()}")
    if time.time() - last > 10:
        print(f"  {seg.end:.0f}/{info.duration:.0f}s", flush=True); last = time.time()

open(OUT_TXT, "w", encoding="utf-8").write(" ".join(plain))
open(OUT_TIMED, "w", encoding="utf-8").write("\n".join(timed))
```

Setup (one-time):
```
py -3.11 -m pip install faster-whisper nvidia-cublas-cu12 nvidia-cudnn-cu12
```
Python 3.11, not 3.14 — ML libs lag the latest Python on Windows.

Run via `Bash` with `run_in_background: true`. The harness re-invokes you when it finishes; no polling, no `ScheduleWakeup`. A 37-min English lecture is ~3-5 min on an RTX 4060 + `large-v3` fp16, ~10-15 min on CPU with `small.en` int8.

### Gotchas (each one cost a real run)

| Symptom | Fix |
|---------|-----|
| `OSError: [WinError 1314]` — symlink perms | HF cache uses symlinks; Windows blocks them without Developer Mode. Use `snapshot_download(local_dir=...)` to bypass. |
| `Library cublas64_12.dll is not found` | Install `nvidia-cublas-cu12` + `nvidia-cudnn-cu12` via pip and call `os.add_dll_directory(...)` on `<site-packages>/nvidia/cublas/bin` and `cudnn/bin` BEFORE importing faster-whisper. |
| Exit code 127 even though files written | Garbage-collection ordering quirk during interpreter shutdown. Trust the output files, not the exit code. Check the file sizes. |
| `Library cublas64_12.dll` re-appears even after install | DLL search-path was registered after import. Move the `os.add_dll_directory` block ABOVE the `from faster_whisper import` line. |
| Transcript has English content but random foreign tokens | Pass `language="en"` explicitly to `model.transcribe()` — auto-detect can drift. |

## Step 3 — summarize the way Praneel wants

He stated it explicitly: *"I want your judgement to teach me."* The summary is a teaching artifact, not a topic list. Hit these sections, in this order:

1. **Thesis in one sentence.** The single central claim the lecture is built around. If you can't compress it, you don't understand the lecture yet — reread before writing.
2. **Concept toolkit table.** When the lecture introduces multiple concepts/frameworks, lay them out as a markdown table — `#`, concept, thinker, one-line insight. Tables beat prose for retention and reference.
3. **The argumentative move worth noticing.** Highest-value section. What is the *rhetorical structure*? Does each framework solve a problem the previous one created? Does the lecturer build by analogy, contrast, escalation, deflation? Name the move. The thing future-Praneel quotes back is the structure, not the content.
4. **Examples used, organized.** List as bullets, tag which concept each example supports. Examples get reused on papers and exams — make them retrievable, not buried in prose.
5. **Three things likely testable / paper-worthy.** Sharpest distinctions the lecturer flagged, common-misunderstanding warnings she paused to correct, dichotomies she explicitly drew (X vs Y). These are exam predictions in plain English.
6. **Lecturer's positionality / register, when given.** If she modeled the analytical move she wants from students (positionality statements, evidence labels, framing register), name what she modeled — that's the assignment rubric in disguise.
7. **Transcription notes.** If Whisper produced obvious artifacts (one phrase repeated 20+ times during silence, garbled stretches), note them at the bottom with the timestamp from the timed transcript so Praneel can verify specific claims against the video.

**Length:** 600-1000 words of substantive summary for a 30-60 min lecture. Less = skim; more = padding. The summary in the conversation that produced this skill landed around 900 — good zone.

## What he hates here

- Generic "this lecture covered X, Y, Z" topic lists.
- Consultant verbs: "explores," "engages with," "considers," "addresses." Use real verbs that say what the lecturer actually *did* — "deflates," "contrasts," "builds on," "concedes."
- Bullets with no through-line — random facts with no argumentative spine.
- Pretending you watched the video when you didn't transcribe it. He flagged this directly: *"if I wrote you a transcript and summary right now, I'd be hallucinating what your professor said."* Don't.

## Register

Skill content follows `taste.md`: short verdicts, long reasoning, concrete nouns. Apply the AMAZING / GOOD / CONSULTANT hierarchy to the summary itself. The thesis line and the "argumentative move" line are the two places to spend AMAZING tier; everything else should land in GOOD.

## Composes with

- **`feedback_output_file_location` memory** — outputs to `C:\Users\prapa\Downloads\`, not home directory.
- **`taste.md`** — the summary is text a human will read; apply the quality bar.
- **Chrome MCP** (`mcp__claude-in-chrome__*`) — for inspecting Canvas iframes, triggering downloads via JS, reading network requests when the file ID isn't obvious from the DOM.
