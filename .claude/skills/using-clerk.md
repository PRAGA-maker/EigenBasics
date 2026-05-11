---
name: using-clerk
description: Use when adding authentication, sign-in/up flows, user management, organizations (B2B / multi-tenant), webhooks, JWT verification, session handling, or RBAC on a project that uses or could use Clerk — any framework. Routes between Clerk's installable Skills, the remote Clerk MCP server, the dashboard via Chrome MCP, and direct docs. Read before installing `@clerk/*` or wiring middleware.
---

# Using Clerk

Clerk's surface area is wide — 15+ framework SDKs, prebuilt + headless components, Backend API, organizations, webhooks, JWT templates, billing. The right answer is rarely one tool. There are **four routes**: Clerk's installable Skills package (per-framework prompts), the remote Clerk MCP server (snippets on demand), the dashboard via Chrome MCP (keys, webhooks, JWT templates, real users), and direct docs (concepts, troubleshooting). Pick by job.

## When to use

Use this skill before:
- Installing any `@clerk/*` package
- Wiring `clerkMiddleware()` / `proxy.ts` / `middleware.ts`
- Designing organizations, roles, or permissions for B2B
- Verifying Clerk-issued JWTs in a non-Clerk backend
- Setting up webhooks for user/org sync to your DB
- Reading or writing the Clerk Backend API

Don't use this skill for:
- Project-internal auth conventions (those go in CLAUDE.md)
- Generic OAuth / OIDC theory questions (Clerk abstracts most of it)

## The four routes

| Route | What it is | Best for | Worst for |
|---|---|---|---|
| **Clerk Skills** (`npx skills add clerk/skills`) | Per-framework + per-feature prompt packages installed into the agent | Actually building. Always start with `/clerk` (the router) | Quick lookups — heavier than MCP |
| **Clerk MCP** (`mcp__clerk__*`) | Remote MCP server returning SDK snippets on demand | Targeted snippet retrieval; framework-agnostic patterns | Multi-step setup; opinionated wiring |
| **Dashboard via Chrome MCP** | dashboard.clerk.com — keys, JWT templates, webhooks, sessions, organizations, application logs, real users | Config that has no API; debugging real session/sign-in failures; reading runtime logs | Anything code-related |
| **Direct docs** (clerk.com/docs) | The full reference + concept guides | Concepts, deprecations, things Skills/MCP haven't packaged yet (e.g. niche edge cases) | Boilerplate — Skills/MCP are faster |

## Auth setup (read first)

Three keys + one webhook secret. **Frontend vs backend separation is non-negotiable** — the secret key grants admin-level access to your Clerk backend API.

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...   # safe to embed in client; prefix varies by framework (VITE_, EXPO_PUBLIC_, PUBLIC_)
CLERK_SECRET_KEY=sk_test_...                     # backend only — NEVER ship to the client
CLERK_WEBHOOK_SIGNING_SECRET=whsec_...           # only when consuming Clerk webhooks
CLERK_JWT_KEY=...                                # only when verifying Clerk JWTs in a non-Clerk backend
```

Get keys: dashboard.clerk.com → instance → **API keys**. The page has a framework picker that emits the correct env-var prefix per SDK. `pk_test_*`/`sk_test_*` = development instance; `pk_live_*`/`sk_live_*` = production.

## Route 1: Clerk Skills (`npx skills add clerk/skills`)

Clerk publishes installable agent Skills. Once added, the agent gets specialized routing via slash-commands.

```bash
npx skills add clerk/skills                          # install all
npx skills add clerk/skills --skill clerk-orgs       # install one
```

Available (as of 2026-05):

| Skill | Use when |
|---|---|
| `/clerk` | **Always start here** — routes to the right sub-skill |
| `/clerk-setup` | Adding Clerk to any framework, fresh install |
| `/clerk-custom-ui` | Custom sign-in/up forms, theming, branding |
| `/clerk-backend-api` | Browsing/calling Clerk Backend REST endpoints |
| `/clerk-orgs` | B2B multi-tenancy, RBAC, verified domains, enterprise SSO |
| `/clerk-testing` | Playwright/Cypress for auth flows |
| `/clerk-webhooks` | DB sync, notifications, real-time events |
| `/clerk-nextjs-patterns` | Server Actions, middleware, caching |
| `/clerk-react-patterns` | Vite/CRA SPA, hooks, protected routes |
| `/clerk-expo-patterns` | SecureStore, OAuth deep linking, Expo Router |
| `/clerk-tanstack-patterns` | TanStack Start `createServerFn`, `beforeLoad` |
| `/clerk-react-router-patterns` | RR v7 `rootAuthLoader`, `getAuth`, SSR |
| `/clerk-astro-patterns` | Middleware, SSR pages, islands, API routes |
| `/clerk-chrome-extension-patterns` | Popup/sidepanel, syncHost, service workers |
| `/clerk-nuxt-patterns` | Middleware, composables, SSR |
| `/clerk-vue-patterns` | Composables, Vue Router guards, Pinia |
| `/clerk-android` | Native Android/Kotlin/Compose |
| `/clerk-swift` | Native iOS/SwiftUI |

When a Clerk Skill matches the framework, **prefer it over the MCP**. It's an opinionated, multi-step recipe; MCP is a snippet vending machine.

## Route 2: Clerk MCP server

Already registered at user scope (`mcp list` shows `clerk: https://mcp.clerk.com/mcp (HTTP) ✓ Connected`). If a fresh agent needs to install:

```bash
claude mcp add clerk --transport http --scope user https://mcp.clerk.com/mcp
```

HTTP transport only — **no SSE**. Currently in beta.

Tools:
- `mcp__clerk__list_clerk_sdk_snippets` — discover what bundles/snippets exist
- `mcp__clerk__clerk_sdk_snippet` — fetch a specific snippet

Pre-curated bundles: `b2b-saas`, `waitlist`, `auth-basics`, `custom-flows`, `organizations`, `server-side`.

Workflow: call `list_clerk_sdk_snippets` first (cheap discovery), then `clerk_sdk_snippet` for the bundle that matches the task. Don't guess bundle names.

Best for: "show me the verifyToken signature in @clerk/backend", "what does the Expo SecureStore bridge look like", "give me the org-switcher snippet". Worst for: "set up Clerk in my Next.js app from scratch" — that's a Clerk Skill (`/clerk-setup`) job.

## Route 3: Dashboard via Chrome MCP

URL shape: `https://dashboard.clerk.com/apps/<app_id>/instances/<instance_id>/<page>`.

| Page suffix | What lives there |
|---|---|
| `api-keys` | Publishable + secret keys, framework-picker `.env` snippets |
| `users` | Real signed-up users, impersonate, manual ban/unban |
| `organizations` | Real orgs, members, invitations |
| `application-logs` | Auth events, webhook deliveries, errors |
| `user-authentication/...` | Configure section: email/SMS/OAuth/SSO providers, attributes, MFA |
| `sessions` | Session lifetime, multi-session, JWT template editor |
| `webhooks` | Endpoint URLs, signing secrets, event filters, replay |
| `jwt-templates` | Custom claim shapes for `getToken({template: '...'})` |
| `account-portal` | Hosted sign-in/up URLs (default when you don't render `<SignIn />` yourself) |
| `instance-settings` | Domains, paths, sign-in/up redirects |
| `plan-billing` | Plan, MAU, billing-related limits |

Use Chrome MCP when:
- The setting has no API (hosted-page domains, JWT template UI, webhook signing-secret rotation)
- Debugging a real sign-in failure: read `application-logs` for the actual event
- Cross-checking that a code change took effect (e.g. "did my JWT template land")
- Sanity-checking that webhook deliveries succeed after a deploy

**Chrome MCP gotchas** (inherited from `using-kimi-for-research`):
1. **Cookie/query-string filter on tool results** — Clerk dashboard URLs include long base64 IDs that the safety filter sometimes flags as `[BLOCKED: Base64 encoded data]`. Strip with `.replace(/[a-zA-Z0-9_]{20,}/g,'<id>')` before logging, or read via chunked `console.log` and `read_console_messages` with a `pattern` filter.
2. **OS keyboard collision in parallel tabs** — `type` actions land only in the foreground tab. If automating multiple instances, use the ClipboardEvent paste pattern from the Kimi skill.
3. **Don't trigger confirm dialogs** — Clerk's "delete user / delete instance / rotate secret" buttons throw modal `confirm()`s that freeze the tab. Read the warning, hand off to the human.
4. **Never extract or paste secret keys** — pk is fine to read (Clerk's dashboard literally says "safe to share"); sk is not. If you need the sk, ask the human to paste into `.env`.

Subagent-first for dashboard ops: dispatch a general-purpose subagent with the *outcome* ("read the last 24h of webhook delivery failures and summarize the top 3 error codes"), not the steps. Keeps long DOM reads out of the main context.

## Route 4: Direct docs

`clerk.com/docs/<framework>/...` for concepts, deprecations, and edge cases the Skills/MCP haven't packaged. Notable:
- `clerk.com/docs/guides/ai/overview` — entry point for the AI tooling story (Skills + MCP + AI prompts)
- `clerk.com/docs/guides/ai/skills` — Skills catalog + install
- `clerk.com/docs/nextjs/getting-started/quickstart` — canonical Next.js install (note: Next.js ≥16 uses `proxy.ts`, ≤15 uses `middleware.ts` — same export, different filename)

Use Grok (`xai_cli.py`) only for fast Clerk changelog / "did this API change recently" lookups. For multi-vendor tradeoffs (Clerk vs Auth0 vs Supabase Auth vs WorkOS), use Kimi (see `using-kimi-for-research`).

## Subagent posture

Three patterns where spawning beats inline work:
- **Multi-framework comparison** ("how would this work in Next vs TanStack vs Expo?") — fan out a subagent per framework with the same prompt, fetching snippets in parallel via the MCP.
- **Dashboard log triage** — give a subagent the dashboard URL and the symptom; let it page through `application-logs` and return a 200-line summary instead of pulling raw DOM into your context.
- **Skill installation + smoke** — `npx skills add clerk/skills` followed by a one-line proof that the new slash-commands appeared.

Outcome-first prompts, not step-lists.

## Testing, red-teaming, security

**Default: Chrome MCP + subagent red-teaming. Not Playwright/Cypress scripts.**

The `/clerk-testing` skill ships Playwright/Cypress recipes — useful as scaffolding, but **don't reach for it first** for auth flows. Reasons:
- Auth UX is highly dynamic (modals, redirects, cross-domain Account Portal, OAuth pop-ups, MFA prompts, rate-limit screens). Playwright scripts go stale every Clerk UI release.
- A scripted test only catches what the author already imagined. A subagent steered through Chrome MCP can adapt mid-flow, follow unexpected redirects, and report on what *actually happened* — including failure modes the spec didn't enumerate.
- For a research repo (this one), test coverage isn't the goal; behavior verification under real conditions is.

**The pattern**: dispatch a general-purpose subagent (`model: opus`) with the *outcome* — not the steps. Let it drive Chrome MCP, observe the live dashboard + the running app, and return a structured report.

```
Subagent prompt outline:
- Outcome: "Verify that an unauthenticated user hitting /admin gets bounced to sign-in,
  then after signing in lands back on /admin with a valid session."
- Tools: Chrome MCP, dashboard.clerk.com (already signed in), application logs
- Deliverable: pass/fail + 5-line reproduction trace + any anomalies observed
```

Write Playwright/Cypress only when (a) CI gating actually requires it, or (b) the flow is so stable and so high-traffic that a pinned script is cheaper than a subagent run. In that case, lean on `/clerk-testing` for the recipe.

### Security audits — always red-team thoroughly

**Anything security-touching gets an explicit audit + red-team pass. No exceptions.** "Security-touching" includes: middleware/route protection, role/permission checks, webhook handlers, JWT verification, session config, custom sign-in flows, RBAC, organization invites, secret-key handling.

Mandatory audit pass — fan these out as parallel subagents:

1. **Static audit** — read every file the change touched. For each, answer: what's the trust boundary, what's the threat, is the trust check at the right boundary?
2. **Active red-team via Chrome MCP** — drive the live app as an attacker:
   - Hit protected routes unauthenticated → expect 401/redirect, not 200.
   - Sign in as user A, try to read/mutate user B's resources by ID swap.
   - For orgs: sign in as a member, try admin-only mutations; try cross-org reads.
   - Forge a webhook POST without the Svix signature → expect rejection.
   - Replay an old webhook → expect idempotency or rejection.
   - Strip the Authorization header / cookie → expect failure, not "default user".
   - Mint or steal a token from one instance, present to another → expect failure.
3. **Secret-handling sweep** — grep the diff for `sk_test_`, `sk_live_`, `whsec_`, `CLERK_SECRET_KEY`. Confirm none are in client-bundled code, public env vars, logs, error responses, or git history.
4. **Dashboard cross-check** — read `application-logs` after the red-team run; verify denied requests show up as auth failures, not silent successes.

Report format: one-line verdict per attack vector + the request/response trace for any that didn't fail closed. Treat ambiguity (e.g. 200 with empty body) as a fail until proven otherwise.

Default red-team budget: ~3 parallel subagents minimum on any auth-adjacent PR. Skipping this because "the change is small" is the most common way auth bugs ship.

## Common gotchas

- **Never put `CLERK_SECRET_KEY` in client code, `NEXT_PUBLIC_*`, `VITE_*`, or any framework's public-env prefix.** Server-only.
- **Webhook signature verification is mandatory.** Clerk signs every webhook with `CLERK_WEBHOOK_SIGNING_SECRET` (Svix-format). If you skip the verify step, anyone who finds your endpoint URL can forge user-creation events into your DB.
- **`auth()` (server) vs `useAuth()` (client) vs `authenticateRequest()` (custom backend).** Wrong one = 401 in prod. The Clerk Skills know which to recommend per framework — don't reach for the wrong helper from memory.
- **Next.js 16+ filename change:** middleware file is `proxy.ts`, not `middleware.ts`. Same `clerkMiddleware()` export. Easy to miss.
- **Account Portal vs custom flows.** If you don't render `<SignIn />` / `<SignUp />`, Clerk redirects to its hosted Account Portal. Decide explicitly which one you want; don't ship "default" by accident.
- **Organizations are first-class.** For B2B, use `/clerk-orgs` and Clerk's org primitives — don't roll your own tenant table on top of users. RBAC and member invitations come for free.
- **`pk_test_*` is for the dev instance only.** Production needs a separate instance and `pk_live_*`/`sk_live_*` keys. Same code, different env file.
- **MCP is beta.** If snippets look stale or wrong, fall back to the Clerk Skill or direct docs and flag the drift.

## When in doubt

Snippet → MCP. Setup or framework-shaped recipe → Clerk Skill (`/clerk` router first). Config without an API, real users, real logs → dashboard via Chrome MCP. Concept or "did this change" → docs (or Grok for changelogs).

If two routes both look right in 30 seconds, fire both as parallel subagents and compare outputs. Spawning is always cheaper than missing.
