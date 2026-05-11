---
name: using-cloudflare-primitives
description: Use when building, deploying, debugging, or comparing anything on Cloudflare — Workers, Pages, R2, KV, D1, Vectorize, AI Gateway, AI Workers, Workflows, Durable Objects, Queues, DNS, WAF, Tunnels, Agents SDK. Routes between four interfaces (wrangler CLI, three remote Cloudflare MCP servers, the dashboard via Chrome MCP, and Kimi for cross-product tradeoffs / OSS alternatives) and codifies the subagent-first pattern for context-heavy ops. Read before reaching for any Cloudflare API.
---

# Using Cloudflare primitives

Cloudflare's surface area is huge and fragmented — the right answer is almost never one tool. This skill picks the right door for each job, avoids the "burn 50k tokens spelunking the dashboard or the API schema" trap, and points at Kimi for tradeoff calls Cloudflare's own surfaces can't make honestly.

## When to use

Anytime the task touches any Cloudflare product (Workers, Pages, R2, KV, D1, Vectorize, AI Gateway, Workers AI, Workflows, Durable Objects, Queues, DNS, WAF, Zero Trust, Tunnels, Stream, Images, Agents SDK, Pub/Sub, Hyperdrive, Containers). Also: when the human asks "is Cloudflare the right choice for X" — that's a Kimi question, not a Cloudflare question; route via Door 4.

## The four doors

| Door | What it is | Best for | Worst for |
|------|------------|----------|-----------|
| **1. wrangler CLI** | the official Workers CLI; talks to your wrangler.jsonc project | Worker code, deploys, secrets, local dev (`wrangler dev`), project-bound resource setup | account-level CRUD with no project; "what should I do?" questions |
| **2. Cloudflare MCPs** | three remote MCP servers (Docs / Bindings / API) | docs Q&A; account-level KV/R2/D1/Hyperdrive CRUD without a project; arbitrary REST calls via Code Mode | one-line ops well-served by wrangler/curl |
| **3. Dashboard via Chrome MCP** | drive `dash.cloudflare.com/<account_id>/...` + Agent Lee | visual config; "given my actual deployed stack, what fits" via Agent Lee; things not in CLI/API | anything fully scriptable — burns context |
| **4. Kimi** | `using-kimi-for-research` skill | "Cloudflare X vs OSS Y vs SaaS Z?"; OSS alternatives scan; multi-vendor tradeoffs | Cloudflare-specific docs (Door 2's Docs MCP is closer to source) |

## Auth setup (read first)

Account ID and API token live in `.env` at the repo root:

```
CLOUDFLARE_ACCOUNT_ID=...   # 32-char hex; visible in any dash URL: dash.cloudflare.com/<account_id>/...
CLOUDFLARE_API_TOKEN=...    # cloudflare.com → My Profile → API Tokens → Create Token
CLOUDFLARE_ZONE_ID=...      # only when scripting against a specific zone (DNS, WAF, Page Rules)
```

To create a token: dashboard → top-right avatar → My Profile → API Tokens → Create Token. Use the "Edit Cloudflare Workers" template for most agent work, or a custom token scoped to exactly what you need (Workers Edit, R2 R/W, DNS Edit, AI Gateway Read, etc.). **Don't use the global API key — it can't be scoped.**

`wrangler login` does an OAuth flow that bypasses the API token and writes creds to `~/.wrangler/`. Fine for interactive use; for headless agent runs, prefer `CLOUDFLARE_API_TOKEN` env var (wrangler picks it up automatically).

Verify: `wrangler whoami`. Should print the account email + ID matching `$CLOUDFLARE_ACCOUNT_ID`.

## Door 1: wrangler CLI

Install: `npm i -g wrangler` (node ≥18 required; the repo machine has v24). Or `npx wrangler@latest <cmd>` ad-hoc.

Most-used commands (run `wrangler <cmd> --help` for full flags):

```bash
wrangler whoami                              # auth check
wrangler init <name>                         # scaffold a Worker project
wrangler dev                                 # local dev server with edge bindings
wrangler deploy                              # ship the current Worker
wrangler tail <worker-name>                  # stream prod logs (long-running — see subagent rule)
wrangler secret put <KEY>                    # set a Worker secret (NOT via .env — .env doesn't ship)
wrangler kv namespace create <name>          # KV
wrangler r2 bucket create <name>             # R2
wrangler d1 create <name>                    # D1
wrangler d1 execute <db> --command "SQL"     # D1 query
wrangler vectorize create <name> --dimensions 768 --metric cosine
wrangler queues create <name>
wrangler pages deploy <dir>                  # Pages
```

Multi-account: pass `--account-id $CLOUDFLARE_ACCOUNT_ID` if `wrangler whoami` shows more than one account.

`wrangler dev` runs the Worker on workerd (the actual prod runtime, open-source) at `http://localhost:8787`. Bindings simulated against on-disk state in `.wrangler/state/`, persisted across restarts: KV, R2, D1, Durable Objects, Queues, Vectorize. Per-binding `--remote` flag routes to live edge resources for what can't be simulated (Workers AI inference, AI Gateway, an already-populated R2 bucket). Use for: iterating Worker code, running D1 migrations locally, reproducing prod bugs with V8 stack traces via `--inspector-port`. Not for: validating AI Gateway routing rules, final pre-deploy validation (use `wrangler deploy` to a preview environment).

**Don't run destructive wrangler commands without explicit human OK:** `wrangler delete`, `wrangler r2 bucket delete`, `wrangler d1 delete`, `wrangler kv namespace delete`. Same rule for `--force` flags. This is `git push --force`-tier irreversible.

`wrangler tail` is a long-running stream. If you'll watch it for more than ~30s, dispatch a subagent with the goal stated as outcome ("watch logs, return any errors mentioning $X") and let it return synthesized results. Don't pipe live tail into the main thread — it burns context.

## Door 2: Cloudflare's three remote MCP servers

Three public remote MCP servers maintained by Cloudflare. Highest-leverage way for an agent to *understand* and *operate on* Cloudflare without burning context on docs scrapes or hand-writing API calls.

| Server | Endpoint | Use it for |
|--------|----------|------------|
| **Documentation** | `docs.mcp.cloudflare.com/sse` | "how do I do X?", "what's the YAML for Y?", "what does this error mean?" — token-efficient docs search. Unauth. |
| **Workers Bindings** | `bindings.mcp.cloudflare.com/mcp` | KV / R2 / D1 / Hyperdrive / Workers CRUD without a wrangler project; "what pairs with R2?" + binding-shape questions. OAuth-scoped to your account. |
| **API (Code Mode)** | `mcp.cloudflare.com/mcp` | discovery + execution against the full Cloudflare REST API (~2,500 endpoints); agent writes JS that queries the schema and chains calls. OAuth-scoped to your account. |

### Registering with Claude Code

Two non-obvious rules — both cost hours when ignored:

1. **Endpoint suffix must match the transport flag.** Cloudflare hosts each server at two paths: `/sse` requires `--transport sse`, `/mcp` requires `--transport http`. Mismatch → `claude mcp list` shows "Failed to connect" or OAuth completes but reconnect silently fails forever.
2. **Pin `--callback-port` on every OAuth-gated server.** Without it, Claude Code uses an ephemeral port for the OAuth callback. Cloudflare ties issued tokens to the exact `redirectUri`, so every restart creates a new credentials entry under a different hash, the client picks the wrong/empty one, and you get "Needs authentication" forever after.

Canonical install (one-time per machine):

```bash
# Docs server — unauth, uses /sse + sse transport
claude mcp add --transport sse  --scope user                       cloudflare-docs     https://docs.mcp.cloudflare.com/sse

# OAuth-gated servers — /mcp + http + fixed callback port (unique per server)
claude mcp add --transport http --scope user --callback-port 3118  cloudflare-bindings https://bindings.mcp.cloudflare.com/mcp
claude mcp add --transport http --scope user --callback-port 3119  cloudflare-api      https://mcp.cloudflare.com/mcp
```

Then `/mcp` → authorize the two OAuth-gated servers → restart Claude Code once. Verify with `claude mcp list` — all three should show ✓ Connected, and the tool list should include real tools (`mcp__cloudflare-bindings__d1_database_query` etc.), not just `authenticate`/`complete_authentication` stubs.

If OAuth is already broken (repeated "Got new credentials, but reconnecting failed"): `claude mcp remove --scope user <name>` for each affected server, then edit `~/.claude/.credentials.json` and set `"mcpOAuth": {}` (preserve the `claudeAiOauth` block verbatim — that's your Claude account token), then re-add with the canonical commands above.

After registration, tool names appear as `mcp__cloudflare-docs__*`, `mcp__cloudflare-bindings__*`, `mcp__cloudflare-api__*`. Use `ToolSearch` with `select:mcp__cloudflare-<name>__<tool>` to load schemas before calling, same pattern as the Chrome MCP.

**Bindings MCP can mutate, not just read.** It exposes CRUD tools (`kv_namespace_create/delete`, `r2_bucket_create/delete`, `d1_database_create/delete/query`, `hyperdrive_config_*`, `workers_list/get`) plus doc search. Use it for account-level resource ops you'd otherwise script via wrangler when there's no `wrangler.toml` project in play. For project-bound work (Worker code, deploys, secrets, local dev), still prefer wrangler — the bindings MCP doesn't touch your filesystem or `wrangler.jsonc`.

**Code Mode (API MCP) note:** the API MCP exposes the entire Cloudflare REST API (~2,500 endpoints) as a typed schema. `mcp__cloudflare-api__search` takes a JS arrow function — you write code that introspects `spec.paths`, filters by tag, pulls request/response schemas — and `mcp__cloudflare-api__execute` runs API calls against your account. Treat it like an LSP for CF: *read* the schema first (cheap), *then* write code (the agent does this; you don't have to hand-write API calls). This is the right tool for "I need to do something the CLI doesn't expose cleanly" or anything that spans multiple products.

**Bundled skills on the MCPs themselves.** Both `cloudflare-docs` and `cloudflare-bindings` expose `migrate_pages_to_workers_guide` as a tool — call it before doing any Pages→Workers migration (the description literally says "ALWAYS read this guide before migrating"). More such `*_guide` tools may be added; check the tool list after registering. Separately, Cloudflare publishes a richer catalog of downloadable Agent Skills at `github.com/cloudflare/skills` — clone the folders into `~/.claude/skills/` to install. Worth a one-pass scan when starting a new Cloudflare-heavy project to see what's pre-built (deploying Workers, configuring WAF, etc.).

**Subagent-first for MCP exploration.** A first-time tour of the Bindings MCP or API MCP can produce 20k+ tokens of schema. Dispatch a subagent with the *outcome* stated ("what's the cheapest binding combo for a low-RPS read-mostly key-value cache with 100MB total?") and have it return the answer + the call sequence. Don't dump the schema into the main thread.

## Door 3: Dashboard via Chrome MCP

The dashboard is not a fallback when CLI/MCP fail — it's a first-class source of signal the other doors can't surface. Wrangler-first when something is scriptable, but **don't sleep on the dashboard**. Subagents make it cheap to visit: the DOM read is 10-30k tokens in a subagent that returns 200, so dispatch one and you pay nothing on the main thread. Default posture: when you're already doing non-trivial Cloudflare work, fire a parallel subagent to do a 2-minute dashboard sweep alongside the main task.

URL pattern: `https://dash.cloudflare.com/<account_id>/<section>`. Substitute `$CLOUDFLARE_ACCOUNT_ID` for `<account_id>`. Common sections:

| Section | URL fragment |
|---------|--------------|
| Account home | `/home/overview` |
| Workers & Pages | `/workers-and-pages` |
| Workers > KV | `/workers/kv/namespaces` |
| Workers > D1 | `/workers/d1` |
| Workers > Queues | `/workers/queues` |
| R2 | `/r2/overview` |
| AI Gateway | `/ai/ai-gateway` |
| Workers AI | `/ai/workers-ai` |
| Vectorize | `/workers/vectorize` |
| Workflows | `/workers/workflows` |
| DNS (per zone) | `/<zone_name>/dns/records` |
| WAF (per zone) | `/<zone_name>/security/waf` |
| Pages | `/pages` |

**Always start with `tabs_context_mcp`** (per the chrome MCP guidelines in the system prompt) — never reuse stale tab IDs. Open a fresh tab per task.

Pattern (lifted from the kimi skill, same gotchas apply here):

```
tabs_create_mcp → navigate(url=`https://dash.cloudflare.com/${CF_ACCOUNT_ID}/<section>`) → wait for load → act
```

The user is already authed in Chrome. Don't re-auth.

### Unique value (only here)

Things that live in the dashboard and nowhere else — these are the reasons to sweep even when the CLI/MCP would technically work:

- **Security Insights** — bot/crawler patterns, WAF rule firing rates, suspicious country/ASN spikes, exposed-credential alerts, leaked-token detections
- **Per-product observability** — request volume + error-rate + p50/p99 latency charts; CPU-time histograms; cold-start counts; sampled real-time logs with filter UI (`wrangler tail` is raw stream, dash is the queryable version)
- **Deployment timelines** — failed builds with full log context, preview URLs, rollback diffs across Workers + Pages
- **Billing / usage** — which Worker is burning your quota, per-product spend trajectory, free-tier cliffs you're about to hit
- **Account warnings + product banners** — feature deprecations, region rollouts, account-level config changes the API doesn't expose
- **Weird errors** — 1101 / 1015 / 1042 internal-error spikes that don't show in your code logs but are visible in the analytics tab
- **Agent Lee** — see below

### Dashboard observations log

When you notice something on a sweep that isn't actionable *right now* but might matter later (a quiet WAF spike, a Worker burning unexpected CPU, a deprecation banner, an R2 size jump, a vector index that hasn't been queried in a month), **deposit it in `context/cloudflare-observations.md`** (create the file on first use; append-only, structured like a `runlog.md`):

```
## 2026-05-11 — <one-line headline>
**Where:** dash URL where you saw it
**What:** the observation
**Why it might matter:** one or two sentences
**Status:** noticed / investigating / handed to subagent #N / resolved
```

For small observations, leave them inline for future-you. For anything bigger ("this Worker has 12x the CPU it should"), dispatch a `general-purpose` subagent (model: opus) to investigate and append findings under the same entry.

**The frame:** this account belongs to a team. The agent's job is to act like a cracked, bias-toward-action, first-principles engineer + PM with real ownership over what's deployed there. Notice things. Write them down. Pick threads up later. High ROI; the only cost is paying attention while you're already there.

### Agent Lee (the in-dashboard agent)

Lee is Cloudflare's first-party "ask my account" agent — it has read access to everything deployed under the current account, plus write ops (DNS / SSL / Workers routes / etc.) gated behind per-action confirm dialogs. **Lee is not externally addressable** — you can only reach it via the dashboard. **Hotpath: "Ask AI" button in the top-right of any dashboard page** — opens a side panel; works from any URL under `dash.cloudflare.com/<account_id>/...`, so just navigate to `/home/overview` and click. Docs: `https://developers.cloudflare.com/agent-lee/`. Use Lee for:

- Holistic "what should I do given what I have" questions
- "What's deployed in this account?" answers without an API tour
- Cross-product reasoning that the API MCP can do but slower
- Cost / quota / utilization questions tied to your specific account state

Don't use Lee for anything you'd be embarrassed about leaking to Cloudflare's logs (it's their hosted agent, not yours).

### Chrome MCP gotchas (inherited from the kimi skill)

These bite the same way on the Cloudflare dashboard:

1. **OS-keyboard collision in parallel tabs.** `mcp__claude-in-chrome__computer` `type` actions all land in the foreground tab. If you're typing into multiple dashboard search boxes in parallel, use the ClipboardEvent paste trick from the kimi skill, not `type`.
2. **Cookie/query-string filter on tool results.** Dashboard pages have many cookied/parameterized URLs in the DOM. Strip `https?://` and `?...` query strings before returning text, or use chunked console-log workaround. See the kimi skill for both patterns.
3. **Don't trigger confirm dialogs.** `Delete`, `Disable`, `Purge` buttons all open browser confirms or modals that block the MCP. If a destructive action is genuinely needed, *warn the human first and have them confirm in chat* before clicking. See the chrome-MCP guidelines in the system prompt.
4. **Screenshot when stuck.** If a step silently no-ops, take a screenshot and look at it before retrying. The dashboard has rate-limit toasts, "feature flag gated" overlays, and modal dialogs that aren't surfaced as errors.

### Subagent-first for dashboard ops

ANY multi-step dashboard task — including the 2-minute sweeps above — should run in a subagent. Reading the DOM of a typical dash page is 10-30k tokens; doing 5 navigations in the main thread eats your budget, while a subagent reads it all and returns 200 tokens. Dispatch a `general-purpose` subagent (model: opus) with the *outcome* stated ("turn on AI Gateway logging for this account; return the gateway ID" / "sweep Security Insights + Workers analytics for anything unexpected and append to `context/cloudflare-observations.md`") and let it return the result. Cheap to fire, high ROI per fire — don't ration them.

## Door 4: Kimi for cross-vendor / OSS tradeoffs

Cloudflare's own surfaces are honest about *Cloudflare* but won't tell you "actually self-hosted Postgres on Hetzner is cheaper for your access pattern" or "the OSS alternative to Workers AI is better-suited here". Kimi can.

**REQUIRED:** Use the `using-kimi-for-research` skill. Don't reinvent the parallel-tab pattern, the Lexical paste-event trick, or the cookie-filter workarounds — they live there.

Two prompt shapes that work well:

> *"I'm considering Cloudflare {X} for {use case with concrete access pattern: RPS, payload size, consistency needs, region}. Compare against {Y OSS} and {Z SaaS}. Cite vendors and authors with specific versions/years. Flag where your knowledge is shallow."*

> *"What OSS primitives could replace Cloudflare {X} for {use case}? Include latency/cost/operational tradeoffs. Surface anything that's a strict win for the user."*

Fire 4 parallel angles (cost, latency, operational burden, ecosystem) — Kimi handles parallel tabs natively.

**Always pair Kimi with Agent Lee when comparing Cloudflare products.** Fire them in parallel (Kimi for cross-vendor + OSS perspective; Lee for "given THIS account's actual stack/usage, what fits") and synthesize. Two inputs, two angles — Kimi can't see your account state and Lee can't see outside Cloudflare. One without the other is half-blind. Skip pairing only when the question is purely OSS-vs-OSS (no CF) or purely intra-CF (no alternative considered).

Don't use Kimi for Cloudflare-specific docs (Docs MCP is cheaper, closer to source, and won't hallucinate).

## Subagent posture (across all doors)

Per `claude.md`, this repo is on a Max plan and 3-5 concurrent subagents per active thread is the **baseline**, not the ceiling. Cloudflare ops in particular benefit:

- **Always subagent for MCP schema tours** (Bindings MCP, API MCP) — schemas are huge.
- **Always subagent for dashboard automation past 2 navigations.**
- **Always subagent for `wrangler tail` runs longer than ~30s.**
- **Subagent-per-product when comparing 3+ products** (one agent per product, each writes a one-page summary, you synthesize).

Spawn the agent with the goal as *outcome* ("deploy a Worker that does X and return its URL"), not as *steps* ("run `wrangler init`, then..."). Per CLAUDE.md, prescribed steps become dead weight when the premise is wrong.

## Common gotchas

- **`.env` doesn't ship to the edge.** Worker secrets must be set via `wrangler secret put <KEY>` or the dashboard. Confused users put `OPENAI_API_KEY` in `.env`, deploy, and get `undefined` at runtime.
- **Account-scoped vs zone-scoped.** Workers/R2/KV/D1 are account-scoped. DNS/WAF/Page Rules are zone-scoped (need `CLOUDFLARE_ZONE_ID`). The dashboard URL tells you which.
- **Workers AI ≠ AI Gateway.** Workers AI = inference. AI Gateway = proxy/cache/log layer in front of any model provider. Often confused; both tools serve different jobs and can be combined.
- **Free-tier limits matter.** 100k req/day on Workers, 10ms CPU on free, 1GB R2 storage, etc. Surface to human before deploying anything that might bill.
- **Durable Objects need migrations.** Adding/renaming a DO class requires a migration entry in `wrangler.toml`. Easy to miss; deploys silently lose old DOs.
- **Region semantics differ per product.** D1 is global with single-writer regions; R2 is jurisdictional (FedRAMP / EU); KV is eventually consistent across regions; Vectorize is per-region. If region matters, check Bindings MCP for the current product's semantics.
- **`wrangler.toml` has TWO config formats.** Older `[env.production]` style and newer `wrangler.jsonc`. Don't mix. New projects: use `wrangler.jsonc` (better tooling, allows comments).
- **Don't paste API tokens into chat or commits.** They authenticate against your account with the scopes granted. Rotate via dashboard if leaked.
- **Cloudflare's Agents SDK** (separate from this skill — it's a thing you build, not a thing you call) lets you deploy stateful AI agents on Workers + Durable Objects. If you're literally building an agent that runs on Cloudflare, use the Bindings MCP to discover the SDK shape rather than guessing.

## When in doubt

> Read or ask → MCP. Write or run → wrangler. Visual or holistic → dashboard + Agent Lee. Cross-vendor or OSS → Kimi. Long output → subagent.

If you can't decide between two doors in 30 seconds, fire both in parallel subagents and compare. This repo's posture is "spawning is always cheaper than missing."
