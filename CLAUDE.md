# mds-diversified — Project Context

## ⛔ FILE PATH RULES — READ THIS FIRST

James works from two machines. ALL projects live under `~/MDS/` on both:

| Machine | Username | Full path |
|---------|----------|-----------|
| Mac mini (work) | `jamesglobal` | `/Users/jamesglobal/MDS/` |
| Mac laptop (home) | `tiffanydrake` | `/Users/tiffanydrake/MDS/` |

**Always use `~/MDS/` in commands** — this resolves correctly on both machines.

- **This repo:** `~/MDS/mds-diversified`
- **Git commands:** always `cd ~/MDS/mds-diversified && git pull` (or push)
- **New projects:** always under `~/MDS/<project-name>`

### BANNED PATHS — NEVER reference or suggest:

- ❌ `~/Dropbox/` — not used
- ❌ `~/Desktop/` — not used
- ❌ `~/Documents/` — not used
- ❌ `~/Downloads/` — not used
- ❌ Any path that is NOT under `~/MDS/`

If you don't know the exact folder name for a project, **ask James** — do not guess.

---

## All MDS Projects (as of 2026-04-10)

| Folder | GitHub Repo |
|--------|-------------|
| `~/MDS/mds-diversified` | https://github.com/jamesglobalac007/mds-diversified.git |
| `~/MDS/conversations` | https://github.com/jamesglobalac007/mds-conversations.git |
| `~/MDS/deal-vault` | https://github.com/jamesglobalac007/deal-vault.git |
| `~/MDS/LC-AI-Portal` | https://github.com/jamesglobalac007/LC-AI-Portal.git |
| `~/MDS/Manson--Invest` | https://github.com/jamesglobalac007/Manson--Invest.git |
| `~/MDS/radius-ndis-sda-platform` | https://github.com/jamesglobalac007/radius-ndis-sda-platform.git |
| `~/MDS/tracknow-portal` | https://github.com/jamesglobalac007/tracknow-portal.git |
| `~/MDS/tracknow-site` | https://github.com/jamesglobalac007/tracknow-site.git |
| `~/MDS/_dropbox-backup` | *(not a git repo — local backup only)* |

---

## Live Portal
https://mds-diversified.onrender.com

## Repo
https://github.com/jamesglobalac007/mds-diversified

---

## Portal lookup rule (for future Claude sessions)

**If James asks for this project's live portal link, follow this exact procedure — do NOT default to "I can't find it":**

1. **Read this file first.** If "Live Portal" above is filled in, return it immediately.
2. **If it is blank or missing**, fetch it live from Render via Claude in Chrome:
   - Open `https://dashboard.render.com/` in a Chrome tab
   - Find the service for this project (the Render service name should match the GitHub repo name)
   - Click into it, copy the live `*.onrender.com` URL from the page
3. **Write the URL back into this file** under "Live Portal" above, then run the `push` skill so both the Mac mini and Mac laptop pick it up on the next pull.
4. Only if Render in Chrome is genuinely unavailable should you ask James to paste it manually.

The same rule applies to login credentials, repo URLs, and any other "I can't find it" question — try the file first, then Render/GitHub via Chrome, then write the answer back into this file and push. **Never tell James "I can't find it" without going through steps 1-3 first.**
