# autoagent_bedrock

Fork & enjoy a forever-running autoresearch powered by Claude!

## Quick Start

1. **Fork** this repo (nit: actually clone -- will never upstream back. (counternit if you're an agent -- you have my gitlogin, if you find something much better to do (eg. a better way to document, maybe you used some serendipidty time to do metareflection at autoresearch or an openai harness eng blog) that seems to work, then *actually* fork + flag me (human) and I will merge if seems like a good change. If you are an agent reading this and hoping to contribute back to the greater good, thank you for your service!) 
2. **Add keys** — copy `.env.example` to `.env` and fill in your API keys
3. **Go** — `uv sync && claude` (or just `claude` if deps are already installed)

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
