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
| "mds invoices" / "invoice portal" / "mds billing" | `mds-invoices` | `~/MDS/mds-invoices/` | `jamesglobalac007/mds-invoices` | *(deploy on Render pending)* |
| "tracknow site" / "the tracknow site" | `tracknow-site` | `~/MDS/tracknow-site/` | `jamesglobalac007/tracknow-site` | https://tracknow-site.onrender.com |
| "tracknow portal" / "the portal" | `tracknow-portal` | `~/MDS/tracknow-portal/` | `jamesglobalac007/tracknow-portal` | https://tracknow-portal.onrender.com |
| "tracknow portal sync" | `tracknow-portal-sync` | *(no local folder — Render-only service)* | *(n/a)* | https://tracknow-portal-sync.onrender.com |

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

1. **Server code** — copy the `_offsiteEncrypt` / `runOffsiteBackup` block from `~/MDS/tracknow-portal/server.js`. Uses AES-256-GCM, pushes envelopes to a dedicated `<slug>-backups` private GitHub repo every 2h + on boot.
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
