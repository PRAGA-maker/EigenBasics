---
name: using-cloudflare-primitives
description: Use when building, deploying, debugging, or comparing anything on Cloudflare — Workers, Pages, R2, KV, D1, Vectorize, AI Gateway, AI Workers, Workflows, Durable Objects, Queues, DNS, WAF, Tunnels, Agents SDK. Routes between four interfaces (wrangler CLI, three remote Cloudflare MCP servers, the dashboard via Chrome MCP, and Kimi for cross-product tradeoffs / OSS alternatives) and codifies the subagent-first pattern for context-heavy ops. Read before reaching for any Cloudflare API.
---

# Using Cloudflare primitives

Cloudflare's surface area is huge and fragmented — the right answer is almost never one tool. This skill picks the right door for each job, avoids the "burn 50k tokens spelunking the dashboard or the API schema" trap, and points at Kimi for tradeoff calls Cloudflare's own surfaces can't make honestly.

## When to use

Anytime the task touches any Cloudflare product (Workers, Pages, R2, KV, D1, Vectorize, AI Gateway, Workers AI, Workflows, Durable Objects, Queues, DNS, WAF, Zero Trust, Tunnels, Stream, Images, Agents SDK, Pub/Sub, Hyperdrive, Containers). Also: when the human asks "is Cloudflare the right choice for X" — that's a Kimi question, not a Cloudflare question; route via section 7.

## The four doors

| Door | Best for | Worst for |
|------|----------|-----------|
| **wrangler CLI** | deploy / run / mutate state / tail logs / local dev | "what should I do?" questions; cross-product comparisons |
| **Docs MCP** (`https://docs.mcp.cloudflare.com/mcp`) | "how do I do X?" / API shapes / config schema | mutating state |
| **Bindings MCP** (`https://bindings.mcp.cloudflare.com/mcp`) | "I already have ABC primitives, what pairs with them?" / KV vs D1 vs Vectorize / "what binding does this need?" | unrelated to bindings (DNS, WAF, etc.) |
| **API MCP / Code Mode** (`https://mcp.cloudflare.com/mcp`) | discover + execute arbitrary REST calls; agent writes TS to query the schema and chain calls | trivial single-call ops (just use wrangler or curl) |
| **Dashboard via Chrome MCP** | visual config, Agent Lee, things not exposed cleanly via API/CLI, debugging from the dashboard's view | anything scriptable — burns context |
| **Kimi via `using-kimi-for-research` skill** | "Cloudflare X vs OSS Y vs SaaS Z?" / "is there an OSS primitive that beats this?" / multi-source tradeoff calls | Cloudflare-specific docs (Docs MCP is cheaper + closer to source) |

**Default rule:** if you're reading or asking → MCP. If you're writing or running → wrangler. If you're configuring something visual or want a holistic "given what I have, what should I do?" answer → dashboard + Agent Lee. If you're comparing across vendors or considering OSS → Kimi.

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

## Door 2/3/4: Cloudflare's three remote MCP servers

These are public SSE/HTTP MCP endpoints maintained by Cloudflare. They're the highest-leverage way for an agent to *understand* Cloudflare without burning context on docs scrapes.

| Server | URL | Use it when |
|--------|-----|-------------|
| **Documentation MCP** | `https://docs.mcp.cloudflare.com/mcp` | "how do I do X?", "what's the YAML for Y?", "what does this error mean?" — token-efficient docs search |
| **Workers Bindings MCP** | `https://bindings.mcp.cloudflare.com/mcp` | "I have R2 + a Worker, what should I add for vector search?", "KV vs D1 vs Vectorize for this access pattern?", "what's the binding shape for X?" |
| **API MCP (Code Mode)** | `https://mcp.cloudflare.com/mcp` | discovery + execution against the full Cloudflare API; the agent writes TypeScript to query schema, chain calls, generate the implementation |

**Registering with Claude Code** (one-time per machine):

```bash
claude mcp add cloudflare-docs https://docs.mcp.cloudflare.com/mcp --transport sse
claude mcp add cloudflare-bindings https://bindings.mcp.cloudflare.com/mcp --transport sse
claude mcp add cloudflare-api https://mcp.cloudflare.com/mcp --transport sse
```

The first invocation of each will trigger an OAuth flow in a browser tab (so Cloudflare can scope the connection to your account). Approve once; tokens persist.

After registration, tool names appear as `mcp__cloudflare-docs__*`, `mcp__cloudflare-bindings__*`, `mcp__cloudflare-api__*`. Use `ToolSearch` with `select:mcp__cloudflare-<name>__<tool>` to load schemas before calling, same pattern as the Chrome MCP.

**Code Mode (API MCP) note:** the API MCP exposes the entire Cloudflare REST API as a typed schema your agent reads, then writes TS that the server runs in a sandbox. Treat it like an LSP for CF — *read* the schema first (cheap), *then* write code (the agent does this; you don't have to hand-write API calls). This is the right tool for "I need to do something the CLI doesn't expose cleanly."

**Subagent-first for MCP exploration.** A first-time tour of the Bindings MCP or API MCP can produce 20k+ tokens of schema. Dispatch a subagent with the *outcome* stated ("what's the cheapest binding combo for a low-RPS read-mostly key-value cache with 100MB total?") and have it return the answer + the call sequence. Don't dump the schema into the main thread.

## Door 5: Dashboard via Chrome MCP

For things that are visual, undocumented in the API, or where Agent Lee's holistic view of your account beats raw doc lookup.

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

ANY multi-step dashboard task should run in a subagent. Reading the DOM of a typical dash page is 10-30k tokens; doing 5 navigations in the main thread eats your budget. Dispatch a `general-purpose` subagent (model: opus) with the *outcome* stated ("turn on AI Gateway logging for this account; return the gateway ID") and let it return the result.

## Door 6: Kimi for cross-vendor / OSS tradeoffs

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
