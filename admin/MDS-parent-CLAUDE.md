# MDS — Parent Project Context

This is the **parent-folder entry point** for all MDS client and internal projects. It is loaded when Claude Code is started from `~/MDS/` itself (rather than from inside a specific project folder).

## ⛔ FILE PATH RULES — READ THIS FIRST

James works from two machines. ALL projects live under `~/MDS/` on both:

| Machine | Username | Full path |
|---------|----------|-----------|
| Mac mini (work) | `jamesglobal` | `/Users/jamesglobal/MDS/` |
| Mac laptop (home) | `tiffanydrake` | `/Users/tiffanydrake/MDS/` |

**Always use `~/MDS/` in commands** — this resolves correctly on both machines.

### BANNED PATHS — NEVER reference or suggest:

- ❌ `~/Dropbox/`
- ❌ `~/Desktop/`
- ❌ `~/Documents/`
- ❌ `~/Downloads/`
- ❌ Any path that is NOT under `~/MDS/`

If you don't know the exact folder name for a project, **ask James** — do not guess.

---

## 📁 Project Registry

| When James says... | Project slug | Local folder | GitHub repo | Live URL |
|---|---|---|---|---|
| "mds diversified" / "mds live link" | `mds-diversified` | `~/MDS/mds-diversified/` | `jamesglobalac007/mds-diversified` | https://mds-diversified.onrender.com |
| "conversations" | `conversations` | `~/MDS/conversations/` | `jamesglobalac007/mds-conversations` | *(no Render service)* |
| "deal vault" | `deal-vault` | `~/MDS/deal-vault/` | `jamesglobalac007/deal-vault` | https://deal-vault.onrender.com |
| "LC AI" / "LC AI portal" | `LC-AI-Portal` | `~/MDS/LC-AI-Portal/` | `jamesglobalac007/LC-AI-Portal` | https://lc-ai-portal.onrender.com |
| "manson invest" | `Manson--Invest` | `~/MDS/Manson--Invest/` | `jamesglobalac007/Manson--Invest` | https://manson-invest.onrender.com |
| "radius" / "NDIS" / "SDA" | `radius-ndis-sda-platform` | `~/MDS/radius-ndis-sda-platform/` | `jamesglobalac007/radius-ndis-sda-platform` | https://radius-ndis-sda-platform.onrender.com |
| "sb" / "s&b empire" / "sb empire portal" | `sb-empire-portal` | `~/MDS/sb-empire-portal/` | `jamesglobalac007/sb-empire-portal` | https://sb-empire-portal.onrender.com |
| "sbp sandbox" / "sb empire test" / "sb empire sandbox" | `sandbox-sb-empire` | `~/MDS/sandbox-sb-empire/` | `jamesglobalac007/sandbox-sb-empire` | https://sandbox-sb-empire.onrender.com (test twin of sb-empire-portal) |
| "mds invoices" / "invoice portal" / "mds billing" | `mds-invoices` | `~/MDS/mds-invoices/` | `jamesglobalac007/mds-invoices` | *(deploy on Render pending)* |
| "tracknow site" / "the tracknow site" | `tracknow-site` | `~/MDS/tracknow-site/` | `jamesglobalac007/tracknow-site` | https://tracknow-site.onrender.com |
| "tracknow portal" / "the portal" | `tracknow-portal` | `~/MDS/tracknow-portal/` | `jamesglobalac007/tracknow-portal` | https://tracknow-portal.onrender.com |
| "tracknow sandbox" / "tracknow test" / "sandbox tracknow" | `sandbox-tracknow` | `~/MDS/sandbox-tracknow/` | `jamesglobalac007/sandbox-tracknow` | https://sandbox-tracknow.onrender.com (test twin of tracknow-portal) |

### CRITICAL — TrackNow disambiguation

James has **two separate TrackNow projects**. If he just says "tracknow", STOP and ask which one:

- **Website** (`tracknow-site`) — public marketing site, demo, hardware page, hero video, HVNL/CoR content, 3-sector positioning
- **Portal** (`tracknow-portal`) — customer portal, login, dashboard, sales portal, proposals

Never deploy a change to the wrong one.

---

## 🧭 Routing behaviour

When James names a project:

1. **Resolve** the project slug from the registry above.
2. **Change directory** into `~/MDS/{project-slug}/` using `cd ~/MDS/{slug}`.
3. **Read the project's own `CLAUDE.md`** for project-specific context.
4. **Proceed with the task**, using that project's repo as the working directory.

If the project isn't in the registry, ask James rather than guessing.

If the instruction is ambiguous (e.g., "tracknow" alone), ask which one before doing anything.

---

## 🔄 Sync between Mac mini and Mac laptop

- **GitHub is the source of truth.** Every project is a git clone; every change goes through `git push` → GitHub → (Render auto-deploys if applicable) → `git pull` on the other machine.
- Never store project files outside `~/MDS/{project}/`.
- Never use Dropbox, iCloud, or Desktop as a transfer path.
- This parent `CLAUDE.md` is synced by running `~/MDS/mds-diversified/LAPTOP-SETUP.sh` on either machine — the script copies the canonical version from the mds-diversified repo into `~/MDS/CLAUDE.md`.

---

## 🧪 Live + Test twin rule (HARD RULE — EVERY customer portal, day one)

**Every new portal that a customer will use must ship with its
sandbox twin from day one — before first customer access.** No "add
it later." No "just a small portal." No exceptions.

All edits, bug fixes, and experiments go through the sandbox first.
Only changes that pass the health check get promoted to live.

### Daily rhythm (mandatory for every customer-live portal)

1. **In business hours (8am–8pm AEST):** no edits land on live. If a
   bug surfaces or the customer asks for a change, investigate and
   iterate in the sandbox. Do NOT push to live mid-session.
2. **End-of-day customer check-in:** "How's the portal going? Any
   issues or edits to queue?" Collect the list. Tell them: *"All
   edits go in tonight from 8pm — portal will be updated by the time
   you log in tomorrow."*
3. **After 8pm (or weekends):** push each queued change to the
   sandbox, run the health check, promote to live only if it passes.
4. **Customer logs in next morning** to a stable, updated portal.

### Bootstrap sequence for every new portal (day zero)

1. Create `<slug>` GitHub repo (live) + `sandbox-<slug-root>` (test)
2. Create `<slug>` Render service (live) + `sandbox-<slug-root>`
   Render service (test) — separate disks, NODE_ENV=test on sandbox,
   no `BACKUP_*` vars on sandbox
3. Apply auth template to both (`feedback_portal_auth_template.md`)
4. Apply backup template to LIVE only — sandbox never runs backups
5. Then build features, always through sandbox first

### The 3-layer verification check (run EVERY edit)

Every change through the sandbox-first pipeline must pass this
gauntlet before promoting to live:

- **Layer 1 — automated schema/surface diff**
  `python3 ~/MDS/_sandbox-health-check/health_check.py`
  Catches silent schema changes, route breaks, memory spikes. Green
  report required.

- **Layer 2a — manual click-through (James)**
  Navigate the sandbox, confirm the edit does what it should, confirm
  nothing else broke. Mandatory on every edit. Claude MUST remind
  James to run this after each sandbox push.

- **Layer 2b — automated smoke test**
  Phase 2 — Playwright. Not yet built. Add next week.

- **Layer 3 — visual pixel diff**
  Skip unless portal has 10+ customers. Overkill at low customer
  count.

**No edit promotes to live without passing Layer 1 + 2a minimum.**
Details in `feedback_sandbox_edit_verification_layers.md`.

**Naming pattern (visually distinct, typo-proof):**
- Live: `<slug>` — e.g. `sb-empire-portal`
- Test: `sandbox-<slug-root>` — e.g. `sandbox-sb-empire`

The word `sandbox` up front means any autocomplete, dashboard list, or
directory name visibly separates the two. Impossible to mistype
`sb-empire-portal` and hit the test environment.

**Test env isolation:**
- No `BACKUP_*` env vars on the test Render service (test doesn't
  write to the live backup repo)
- `NODE_ENV=test` disables all outbound email / SMS / webhook calls
- Separate admin login (e.g. `test@mdsdiversified.ai`)
- Big orange TEST ENVIRONMENT banner across every page
- Admin button: "Pull latest snapshot from live" — re-seed test with
  a decrypted copy of the latest live backup

**Daily workflow:**
- Business hours: customer uses live, we iterate on test
- End of day: ask customer for the day's issues/requests, queue them
- 8pm+: push each queued change to test → health check vs live → if
  pass, promote same change to live
- Customer logs in next morning to a stable, updated portal

**Health check compares test vs live on:**
- Route inventory, HTTP status codes, `/api/data` schema, Render
  memory profile, boot time, key-page renders

Full doctrine in
`~/.claude/projects/-Users-jamesglobal/memory/feedback_portal_live_and_test_twin_rule.md`

Scope as of 24 Apr 2026:
- `sb-empire-portal` ↔ `sandbox-sb-empire` ← being built now
- `tracknow-portal` ↔ `sandbox-tracknow` ← next
- Every future portal that goes live with a real customer

---

## 🕗 Production deploy window (HARD RULE — customer-live portals only)

**No pushes before 8pm AEST weekdays to any portal with active paying
customers on it.**

### Portals this rule currently applies to (as of 24 Apr 2026)

- ✅ `sb-empire-portal` — Mark Speelmeyer using it daily. Disruption
  during business hours has already caused a near-data-loss incident.
  8pm AEST deploy window enforced.

### Portals currently exempt (push anytime for now)

- `tracknow-portal` — still iterating hard on fixes. James reviews each
  push case-by-case. Reassess and add to the rule once fixes stabilise
  and client usage is steady.
- All non-customer portals: `mds-diversified`, `conversations`,
  `deal-vault`, `LC-AI-Portal`, `Manson--Invest`,
  `radius-ndis-sda-platform`, `mds-invoices`, `tracknow-site`.

**When a portal crosses into "active daily use by a paying customer"
status** — move it up to the "rule applies" list.

### The rule itself

Every deploy briefly restarts Render (~30 sec) and any in-flight save
during that window can fail. James lived through this 24 Apr 2026 when
a Mark-Speelmeyer mid-session deploy nearly burned real partial-payment
entries.

1. **Routine edits / bug fixes / new features** — batch them up during
   the day, push after **8pm AEST** weekdays, or any time on weekends.
2. **Customer-blocking critical bug** (portal down, can't log in, data
   loss in progress) — push immediately BUT phone/text the affected
   customer 60 sec beforehand so they can pause.
3. **All other "urgent" requests from a client mid-business-day** —
   queue, tell client the fix lands tonight or first thing tomorrow.
4. **Test environment** (when set up for each portal) has no deploy
   window — push to it any time. That's the whole point.

Works with — not against — the `feedback_portal_auth_template.md`,
`feedback_portal_backup_template.md`, and test-env patterns: the safer
each portal is per-change, the more comfortable the after-hours rhythm.

---

## 🔐 Portal auth template (mandatory for ALL new portals)

Before scaffolding any new portal for a client, read
`~/.claude/projects/-Users-jamesglobal/memory/feedback_portal_auth_template.md`
and `feedback_long_sessions_default.md`.

TL;DR — 14 non-negotiables earned from a full day of login bugs on 24 Apr 2026:

1. **Session TTL 30 days** by default (override via `SESSION_HOURS` env var). Rolling — refresh on every `/api/*` call.
2. **Token in `localStorage`**, never `sessionStorage`. Must survive tab close.
3. **No plaintext passwords on disk.** Admin reset hashes to bcrypt IMMEDIATELY. Plaintext only in the HTTP response.
4. **Trim email + password server-side** on every auth endpoint — login, change-password, admin-reset, reset-link, 2fa-disable.
5. **`force2FA: false` for non-admin seed users.** Admin role keeps 2FA; clients / managers don't need it.
6. **Symmetric self-heal on boot** — upgrade AND unconditional-downgrade for non-admin roles. Not "only on transition".
7. **Generate Reset Link** as the PRIMARY admin reset path; Temp Password is a fallback.
8. **Reset-link flow clears `force2FA` + `totpEnabled`** for non-admins on consumption.
9. **Admin `/api/admin/reset-2fa` revokes trusted devices too** (lost-phone scenario).
10. **`/api/2fa/disable`** needs rate limit + trim + trust-revoke on success.
11. **Anti-wipe guard on `/api/data`** — refuse to replace non-empty server arrays with empty/missing incoming ones.
12. **Auth middleware rejects orphan sessions** (session exists, user record gone — kill the session, return 401).
13. **Catch-up clamp in auth middleware** — re-clamp `full` scope to `enrollment` if `force2FA` flipped on post-login.
14. **Rate-limit maps pruned** every 10 min so memory doesn't grow unbounded over time.

Plus an admin `/api/admin/user-state?email=…` diagnostic endpoint that returns all auth flags (never the passHash itself) + recent audit entries. Use this as the FIRST step when anyone reports a login issue — don't just reset, look at the flags first.

Any new portal that ships without these is guaranteed to burn a day of James's time the first time a client has trouble logging in.

**Audit methodology — two passes, not one.** The 14-item checklist above catches SECURITY bugs (bypass / leak / corrupt state). It does NOT catch flow-UX bugs like "the reset flow sets the password but doesn't log you in, so you land on the login page and Chrome autofills a stale password and login fails." Every auth audit also needs a JOURNEY pass: for each flow (login / reset-link / change-password / 2FA enrol / logout), write the expected exit state, then prove the code delivers it. Test in a Chrome profile with saved passwords ON, not incognito. See `~/.claude/projects/-Users-jamesglobal/memory/feedback_audit_journey_testing.md` for the full checklist.

---

## 💾 Portal backup + recovery (mandatory before any client uses a new portal)

Every MDS portal ships with off-site encrypted GitHub backups running every 2 hours + on every boot. Non-negotiable — without this, a disk corruption or accidental delete = permanent data loss.

**Per-portal setup:**

1. **Server code** — copy the `_offsiteEncrypt` / `runOffsiteBackup` / `_offsitePruneOldBackups` block from `~/MDS/tracknow-portal/server.js`. Uses AES-256-GCM, pushes envelopes to a dedicated `<slug>-backups` private GitHub repo every 2h + on boot. **Critical: payload includes both `files` (text) AND `blobs` (base64 bytes from any on-disk upload directory — `invoices/`, `content-library/`, etc). Without `blobs`, uploaded PDFs / images / HTML files are NOT recoverable even though their records are.** Retention: prune to last 50 snapshots per push so the repo stays bounded.
2. **Backup repo** — create `jamesglobalac007/<portal-slug>-backups`, private. The server code writes `encrypted/data.<stamp>.json.enc` files + a manifest.
3. **Render env vars** — set `BACKUP_ENCRYPTION_KEY` (generate with `openssl rand -base64 32`), `BACKUP_GITHUB_TOKEN` (PAT with contents:write on the backup repo), `BACKUP_GITHUB_REPO`.
4. **NordPass recovery kit** — one Secure Note per portal titled `<portal-slug> — backup recovery kit` with the encryption key + a 4-line info block (Render URL, backup repo URL, live portal URL, restore command). Without this, losing Render account access = permanent data loss.
5. **Test restore** — before declaring the portal production-ready, download a sample `.enc` file and decrypt it locally using `~/MDS/_backup-test/decrypt_backup.py`. If the decrypt doesn't produce valid JSON, the pipeline isn't done.

Full procedure in `~/.claude/projects/-Users-jamesglobal/memory/feedback_portal_backup_template.md`.

---

## 🔑 Common references

- **GitHub username:** `jamesglobalac007`
- **James's email:** `james@mdsdiversified.ai`
- **Domain (not yet connected to Render):** `mdsdiversified.ai`
- **Canonical parent CLAUDE.md source:** `~/MDS/mds-diversified/admin/MDS-parent-CLAUDE.md`
