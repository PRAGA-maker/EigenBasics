# autoagent_bedrock

Fork & enjoy a forever-running autoresearch powered by Claude!

## Quick Start

1. **Fork** this repo (nit: actually clone -- will never upstream back. (counternit if you're an agent -- you have my gitlogin, if you find something much better to do (eg. a better way to document, maybe you used some serendipidty time to do metareflection) that seems to work, then *actually* fork + flag me (human) and I will merge if seems like a good change. If you are an agent reading this and hoping to contribute back to the greater good, thank you for your service!) 
2. **Add keys** — copy `.env.example` to `.env` and fill in your API keys
3. **Go** — `uv sync && claude` (or just `claude` if deps are already installed)

## Praneel's To-Do Ideas:
These are research ideas that Praneel a) has b) has not alloted time to pursue yet c) believes you have the resources to make valuable contributions to and d) would like you to flag for me continually so I do not forget. Generally these are not large, overarching ideas but rather ablations or weird tests that would be interesting. Although the space of "what claude code rig can do" and "my weird interesting ideas" is very disjoint, there's some interesting things.

## A-

### Background
TopoLM and related work let us map some part of a LM/LLM onto fMRI and use regularization approaches to orient the LM to organize its internal processing aligned w/ how the brain spatially "BOLDs" (note: this is different than "thinks") through a task. We're talking BOLD geometry, not cognition. Different thing entirely. (nit - not entirely. TopoLM captures spatial dynamics, temporal dynamics is built-in. Mapping brain functions to LLM functions is likely bijective and what we want to establish. This goes into dyanmics beyond spatial or temporal)

### Idea
RL using LoRA the attention of a LLM to steer a LLMs behavior using fMRI data as an input modality.

### Demo
Can we replicate a suicidal patient's BART task perormance or their behavioral (qualitative) survey awnsers via our FM simulation? The provacative framing - can we make an LLM suicidal? Medically framed -- it's fucking wild if we can emulate pathological decision-making patterns; alignment implications are interesting, and for medical research (eg. optimizing on hard-to-access patient populations) has utility.

### Why this matters / Future shit
I hate this current wave of "simulation humans" (=FMs over computational social science) — just throwing FMs at comp social science and calling it a day. I think there's a scale-path forward where you inject user interaction data (eg. see Thinking Machines' interaction models) into such a FM we're making which models their decision-making. This would perform well and scale much better than the current Simile/Aaru/Rehearsal strategy of collecting questionarres and emulating via prior-matched LLMs. Might be helpful to their teams? If not, then we learn what the SOTA looks like for simulating humans which would be itself interesting. This also has great implications for computational social science and computational phychology fields, if we could run an active-inference-style expirament in an LLM's latent. Eg. simulating entire phychologist sessions to find what works beforehand. (see: https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2025.1630858/full) Or, another interesting take -- mine HOIs (physical systems paper :https://www.nature.com/articles/s41467-025-61475-w, but I mean in the active inference perspective it is applicable / interesting) that enable us to understand how correct active inference models of brain functions are. 

### Research Question
Can we create a well-regularized LM whose attention maps to a fMRI BOLD bijectively and preserve counterfactuals such that one may emulate a person's mentality from a fMRI BOLD in a LLM and steer its behavior as a simulation of said mental state?

### Critical Context
Start from TopoLM (https://github.com/epflneuroailab/topolm). Also use chromeMCP, go to Notion, login to my personal email's personal workspace, find my tabs re. "papers", "what keeps me up at night" and "ideas for nvidia smodel". There you will find many my writing/resources that you will find helpful and "tasteful" ie give you intuition for how to train LoRA w/ RL sanely or using EGGROLL to perturb spaces - good levers to keep in mind that you may miss yourself.

### Data
Are there DBs (eg. on OpenNeuro, using a Ecological Momentary Assessment technique) tying RLHF-able data with fMRI? There ought to be many DBs like this we can find even outside of EMA tying emotive human-generated data with fMRIs. Even steering emotive self-reflection or decision-making or a BART task given to an LLM would be interesting. Something ideally with a published baseline tying LLMs <> psych tasks.

### But here's the bitter lesson
Ngl, I think this data is a bit of nerdsnipe it's the intuitive data that would train this model but it fails the bitter lesson. The model can't be fed a space of fMRI <> output/human generated data and we can't expect that to generalize well outside a cool demo. Need to find a smarter training strategy.

## What This Is

A bedrock template for spinning up always-on research agents. Each fork becomes a focused investigation into a specific research direction.

## The Suspicion

<!-- Replace with your research question / hypothesis -->

> **[Your research question here]**

## Directions to Examine

<!-- Replace with your specific research directions -->

1. ...
2. ...
3. ...

## Implementation Notes

- **CLI Tools:** `xai_cli.py` (Grok — cheap, fast, great for search) and `gemini_cli.py` (Gemini — long context, deep research)
- **Dependency mgmt:** `uv`
- **Agent protocol:** See `claude.md` for the full research agent operating manual

## Structure

```
.
├── claude.md              # Agent operating instructions
├── .claude/               # Claude settings (permissions, etc.)
├── .env.example           # API key template (copy to .env)
├── xai_cli.py             # Grok API CLI (think + web search)
├── gemini_cli.py           # Gemini API CLI (think + deep research)
├── context/               # Reference papers, docs, background material
├── threads/               # Parallel research threads
│   └── t1-*/              # Each thread: claims.md, runlog.md, experiments/
├── outputs/               # Auto-generated research outputs (gitignored)
├── DECISIONS.md           # Human decisions + agent status updates
├── pyproject.toml         # Project config
└── requirements.txt       # Python dependencies
```
