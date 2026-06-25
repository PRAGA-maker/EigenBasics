---
name: conference-recording-deep-dives
description: Use when given a multi-talk recording (a conference/symposium session, an OBS capture of a livestream, a multi-hour video with several back-to-back speakers) and asked which talks matter for our work and to write them up as deep notes — not a single-lecture summary. Triggers: "here's a recording of [conference], find the talks relevant to us", "which of these talks matter, explain them", "make .mds for the interesting/good ones", a 2–3 hr capture with several presenters.
---

# Conference recording → deep-dive talk notes

## Overview
Turn a raw multi-talk recording into (a) a relevance-ranked map of **every** talk and (b) standalone deep-dive `.md` notes for the **few that matter to our work**. Two failure modes to avoid: treating the whole file as one lecture, and summarizing from the title/agenda without transcribing. Core principle: **transcribe locally → segment into talks → web-verify every speaker (Whisper garbles names) → judge relevance against our ACTUAL research context → deep-dive only the high-relevance talks, grounded in the speakers' real papers, with an intuition layer so a working scientist understands what was actually done.**

**REQUIRED SUB-SKILL:** Use `summarizing-lecture-videos` for the get-video + GPU-transcribe mechanics (the faster-whisper `large-v3` script, the Windows CUDA DLL gotchas, output to Downloads). This skill is the multi-talk + relevance-filter + deep-dive layer on top of it.

## When to use
- A recording with multiple back-to-back speakers (conference session, symposium, seminar series, panel).
- Praneel asks "which talks are relevant to our work and explain them," or "make .mds for the interesting ones."
- An OBS capture of a livestreamed session (find the file via OBS config — Phase 0).

## When NOT to use
- A single lecture → just use `summarizing-lecture-videos`.
- He wants a quick skim / topic list → give that, skip the pipeline.

## Pipeline

**Phase 0 — Locate the recording.** OBS records to the path in `%APPDATA%\obs-studio\basic\profiles\<profile>\basic.ini` → `[SimpleOutput] FilePath` (or `[AdvOut] RecFilePath`). Latest file by mtime is usually it; sanity-check duration against the cue ("the 3-hr one from this morning": started ~06:01, last-written ~09:04 ≈ 3 h).

**Phase 1 — Transcribe locally on GPU (see sub-skill).** Run the faster-whisper `large-v3` fp16 script in the background; **stream the timed transcript to disk as segments arrive** so a long run preserves partial progress. Produce both a plain and a `[MM:SS]`-timestamped transcript in `Downloads\`. Exit code 127 with files written = benign shutdown quirk → trust the files, check sizes.

**Phase 2 — Load OUR research context.** Read the company/research repo (`Documents/github/engram_context`: `README.md`, `context/primer.md`, `context/{company,domain,modeling}/`, `threads/CROSS_THREAD_SYNTHESIS.md`) so relevance is judged against the real thesis, not generic "AI-for-bio." Write down the **relevance lens** — the specific topics/methods that map to our program (e.g. virtual-cell architecture, perturbation prediction, cell-state/fate dynamics, annotation, multimodal/spatial, confounders/interpretability, generative heads).

**Phase 3 — Segment into talks.** Grep the timed transcript for speaker-intro anchors ("our next speaker is…", "will be talking about…", "next up…", and applause/"thank you" boundaries) plus topic shifts. Build a talk table: start time, speaker-as-heard, title-as-heard. Watch for **coffee breaks** (long silent gaps with no segments) and **multi-speaker panel Q&A blocks** (not a talk). Slice the transcript into one file per talk by line range; spot-check each slice's first/last line.

**Phase 4 — Resolve speakers.** Whisper garbles proper nouns. **Web-verify every name + affiliation + their known work** and correct the garble (real examples: "Harmonets"→Harmanec, "Ziller"→Siller, "Payer"→Pe'er, "Sakuna"→Inês Cunha, "Space Traveler"→SpaceTravLR). Never invent — mark unresolved names uncertain.

**Phase 5 — Fan out summaries + relevance verdicts (workflow).** One agent per talk: read its slice + the relevance lens, web-verify the speaker, return a **structured** summary (thesis, concept table, argumentative move, examples, takeaways) **plus a relevance tier HIGH/MED/LOW** with a "why" tied to our work specifically. Synthesize into one ranked briefing (scoreboard table → HIGH deep, MED concise, LOW one-liner → cross-talk synthesis).

**Phase 6 — Deep-dive the HIGH talks.** One standalone `.md` per high-relevance talk, following the template below.

**Phase 7 — Adversarial paper check (do NOT skip).** For each deep-dive, **fetch the speaker's actual papers** (arXiv/bioRxiv/DOI) and extract real methods/data/results. **Flag every talk-vs-paper discrepancy**: claims in the talk absent from the paper, overstated "beats SOTA" (check the *margins* — often thin on real data, bigger only on synthetic), corrected IDs/names. Mark anything unverifiable "(talk-only, unverified)." Be a skeptic, not a stenographer.

## Deep-dive `.md` template (the reusable output shape)
1. **Header** — speaker (verified), affiliation+lab, talk title, timestamps, source file, relevance tier.
2. **Thesis in one sentence.**
3. **Why this matters to us** — tie to specific pieces of our program.
4. **The argument, as built** — the rhetorical/structural move worth quoting back.
5. **Concept toolkit** — table (`# | concept | who | insight`).
6. **Examples / Q&A gold** — concrete, retrievable, with timestamps.
7. **Intuition — read before the methods.** Plain-language mental model + analogies; for a method, a "**but real X does Y → so they add Z**" table showing how each technical piece serves the one core claim. *Always include this* — it's what makes the technical section legible (it's the section Praneel asked for by name).
8. **Methods, data & results — for the working scientist.** From the actual papers: a **Data** table (dataset | what it is/modality/size | source/accession | role), **how the model works** (architecture + the real objective/math), **training setup**, **results that matter** (concrete numbers, what it beat, the metric), **limitations**, **reproduction pointers** (corrected IDs, repos, minimal dataset to try first).
9. **Three things to take to our bench** — a method to borrow, a baseline to beat, a pitfall to avoid, people/labs to contact.
10. **Honest gap** — why it does / doesn't transfer to us.
11. **References & code** + **Transcription caveats** (garbles corrected, talk-only flags).

## Register
Follow `taste.md` and the sub-skill's "what he hates": short verdicts, concrete nouns, real verbs (derives / ablates / convolves / propagates) — **banned**: explores / leverages / engages with / delves. The Intuition section may use analogies; everything else stays tight. Adversarially verify — an unverified claim is *labeled*, not asserted.

## Common mistakes
| Mistake | Fix |
|---|---|
| Summarizing from the title/agenda | Transcribe first — always. Pretending you watched is the cardinal sin. |
| Trusting Whisper's names | Web-verify every speaker; proper nouns garble badly. |
| Treating the whole file as one talk | Segment on intros / breaks / panels first. |
| Generic relevance ("AI for bio, neat") | Judge against the real research context (Phase 2). |
| Repeating the talk's claims as fact | Read the papers; flag talk-vs-paper gaps; check "beats X" margins. |
| Acting on a false premise | If asked "extract speaker X's talk" and X isn't in the recording, **say so and stop — don't fabricate from the closest match.** Verify the conditional before acting. |
| Methods dump with no intuition | Add the Intuition section; show how each technical piece serves the one core claim. |

## Output location
Per the `feedback_output_file_location` memory, write artifacts to `C:\Users\prapa\Downloads\`. Group a recording's deep-dives in a subfolder (e.g. `Downloads\interestingtalk\`) and keep the ranked briefing at the Downloads root.

## Composes with
- `summarizing-lecture-videos` (REQUIRED) — get-video + GPU transcription + the single-talk teaching-summary format.
- `feedback_output_file_location` memory — outputs to Downloads.
- `taste.md` — quality bar for everything a human reads.
- A research workflow (`Workflow` tool) for the Phase-5 fan-out and Phase-7 paper digs.

---
*Validation note: this skill captures a pipeline executed end-to-end and accepted in one session (recording → two HIGH-relevance deep-dives Praneel was reading). It has NOT been put through formal subagent baseline/pressure testing per `writing-skills`. If it ever misfires, pressure-test Phases 3–4 (segmentation/name-resolution) and Phase 7 (paper-vs-talk skepticism) — those are the judgment-heavy steps.*
