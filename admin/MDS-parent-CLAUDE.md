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

## 🚨 AUTO-PUSH RULE — non-negotiable

**Claude MUST automatically commit and push every change to GitHub, without being asked.**

James works from two machines (Mac laptop + Mac mini) and pulls changes on whichever one he's using next. If changes sit uncommitted or unpushed on one machine, the other machine has no idea they exist. This is the #1 source of "where did that fix go?" lost time.

### What this means in practice

1. **After every meaningful code/content change**, Claude must immediately:
   - `git add` the modified files (specific files, not `git add -A` blanket)
   - `git commit` with a clear message explaining WHY (not just what)
   - `git push origin <branch>` — usually `main`

2. **James never has to say "push" or "commit" or "save to GitHub"** — it is the default behavior after every change. He should only ever say "don't push yet" if he wants to pause it.

3. **At the end of every session**, before saying anything like "done" or "handing back", Claude must run `git status` in every active MDS repo touched during the session and push anything dangling. If any repo has staged/unstaged/unpushed changes, push them or explicitly flag them with a reason they're being held back.

4. **If a push fails** (pre-commit hook error, conflict, network), surface it immediately in plain language. Never leave James thinking something was pushed when it wasn't.

5. **Multi-file/multi-repo sessions**: run the end-of-session check across *every* MDS project, not just the one being actively worked on. Git-add + commit + push each repo that has changes.

### Why this rule exists

James asked for it 19 April 2026 after the S&B Empire DocuSeal integration session — several commits tonight would have been stranded on the laptop without explicit "push" commands. This rule makes sync automatic.

### What NOT to do

- Don't ask "do you want me to push?" — just push.
- Don't commit files that contain secrets (API keys, passwords, credit card details). If a secret got into the codebase, flag it and remove it instead of pushing.
- Don't `git add -A` blindly — be specific about what's being committed so noise (temp files, IDE settings, Desktop scratch files) doesn't land in the repo.
- Don't skip the push if the commit succeeds but the push fails — retry or surface the error.

---

## 🔑 Common references

- **GitHub username:** `jamesglobalac007`
- **James's email:** `james@mdsdiversified.ai`
- **Domain (not yet connected to Render):** `mdsdiversified.ai`
- **Canonical parent CLAUDE.md source:** `~/MDS/mds-diversified/admin/MDS-parent-CLAUDE.md`
