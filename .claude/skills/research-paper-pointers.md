---
name: research-paper-pointers
description: Use when identifying a research paper as load-bearing for analysis (multiple citations, anchor role, or subagent handoff). Download the PDF into context/papers/ with a standard naming convention before building claims on it. Prevents imprecision from working off summaries.
---

# Research paper pointers

When you identify a paper as genuinely load-bearing for your analysis — you will cite it more than twice in notes, build architecture decisions around it, pass it to a subagent for synthesis, or make claims that depend on specific details (N, effect size, methods, population) — **pull the PDF into `context/papers/` before you rely on it**. Summaries inferred from another agent's (or your own) description are frequently wrong about the details that matter.

## When to pull a PDF

A paper is load-bearing if ANY of:
- You will cite it >2 times in notes or the writeup
- You are calling it an "anchor," "benchmark," or "foundational reference"
- You are passing its content to a subagent for analysis
- You are making claims about specific details: sample size, exact method, population inclusion criteria, effect size, parameter values, brain regions, etc.

A paper is **not** load-bearing if you only need to confirm a topic exists and drop one citation. For those, a text reference is fine.

## Finding URLs

Try in order:

1. **Lab/author page** — `gershmanlab.com/pubs/`, `pitt.edu/~<username>/`, personal Princeton/Harvard/etc pages. Often the fastest and cleanest PDF. Example: `https://gershmanlab.com/pubs/Millner19.pdf`.
2. **Open-access journal DOI** — PLOS, eLife, Frontiers, Computational Psychiatry, Nature Communications all have direct PDF links. Pattern for PLOS: `https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.XXXXXXX&type=printable`. For Computational Psychiatry (cpsyjournal.org): `https://cpsyjournal.org/articles/10.5334/cpsy.<n>/galley/<id>/download/`.
3. **PMC** — for NIH-funded work. Pattern: `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/pdf/<filename>.pdf`. Check first — sometimes the article lists a direct PDF URL in the sidebar.
4. **Preprint servers** — arXiv (`https://arxiv.org/pdf/<id>`), bioRxiv (`https://www.biorxiv.org/content/10.1101/<id>.full.pdf`), PsyArXiv, OSF Preprints.
5. **Institutional repository** — university research portals (e.g., `pure.ulster.ac.uk`, `escholarship.org`, etc.).
6. **Google Scholar** — click the paper, then use the right-column PDF link if present.

**Never use Sci-Hub or similar.** If a paper is truly paywalled with no open version, note that in the research doc and work from a summary with an explicit "summary-only, PDF not verified" flag.

## Naming convention

`{lastauthor}{year}_{keyword}.pdf` — lowercase, underscores, no spaces.

Examples:
- `millner2019_active_escape.pdf`
- `pedersen2021_aac_ddm.pdf`
- `dombrovski2013_reward_attempters.pdf`
- `karvelis2022_active_inference_suicide.pdf`
- `kleiman2017_realtime_si.pdf`

The `keyword` should be whatever you'll search for when you need to find the paper again — usually the main construct or method, not a generic description.

## Verify after download

PDFs downloaded from landing pages or paywall redirects sometimes arrive as HTML. Verify:

```bash
# Check it's really a PDF
file context/papers/<filename>.pdf
# Or check the magic bytes
xxd -l 8 context/papers/<filename>.pdf   # should start with "%PDF-"
# Quick size check — HTML landing pages are usually <10KB
ls -la context/papers/<filename>.pdf
```

Then use `Read` with `pages: "1-3"` to confirm the title, authors, and abstract match what you expected.

## Reference in notes

Cite with PDF path alongside the bibliographic reference:

> **Millner et al. 2019** (`context/papers/millner2019_active_escape.pdf`) — RL-DDM of active escape bias, n=85 STB veterans + 44 psychiatric controls. Shneidman-theory anchor, no brain imaging.

This makes it trivial for future-you (or another agent) to re-read the source rather than propagating a summary.

## Batch when possible

If you've identified 4-5 load-bearing papers in one synthesis session, fire `curl` calls in parallel within one Bash message — much faster than sequential downloads.

## Red flags that the PDF you downloaded is wrong

- File size <50KB → probably an HTML landing page or error page
- First-page title doesn't match the citation
- Reading gives PDF syntax errors → it's not actually a PDF
- Abstract mentions a completely different topic
- The paper is dated after the year in the citation (might be a different paper by same authors)

When any of these fire, delete and refetch via a different URL path.
