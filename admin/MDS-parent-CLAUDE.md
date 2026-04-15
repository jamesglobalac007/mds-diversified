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
| "mds diversified" / "the website" | `mds-diversified` | `~/MDS/mds-diversified/` | `jamesglobalac007/mds-diversified` | https://mds-diversified.onrender.com |
| "conversations" | `conversations` | `~/MDS/conversations/` | `jamesglobalac007/mds-conversations` | *(see folder CLAUDE.md)* |
| "deal vault" | `deal-vault` | `~/MDS/deal-vault/` | `jamesglobalac007/deal-vault` | *(see folder CLAUDE.md)* |
| "LC AI" / "LC AI portal" | `LC-AI-Portal` | `~/MDS/LC-AI-Portal/` | `jamesglobalac007/LC-AI-Portal` | *(see folder CLAUDE.md)* |
| "manson invest" | `Manson--Invest` | `~/MDS/Manson--Invest/` | `jamesglobalac007/Manson--Invest` | *(see folder CLAUDE.md)* |
| "radius" / "NDIS" / "SDA" | `radius-ndis-sda-platform` | `~/MDS/radius-ndis-sda-platform/` | `jamesglobalac007/radius-ndis-sda-platform` | *(see folder CLAUDE.md)* |
| "tracknow website" / "the tracknow site" | `tracknow-site` | `~/MDS/tracknow-site/` | `jamesglobalac007/tracknow-site` | https://tracknow-site.onrender.com |
| "tracknow portal" / "the portal" | `tracknow-portal` | `~/MDS/tracknow-portal/` | `jamesglobalac007/tracknow-portal` | https://tracknow-portal.onrender.com |

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

## 🔑 Common references

- **GitHub username:** `jamesglobalac007`
- **James's email:** `james@mdsdiversified.ai`
- **Domain (not yet connected to Render):** `mdsdiversified.ai`
- **Canonical parent CLAUDE.md source:** `~/MDS/mds-diversified/admin/MDS-parent-CLAUDE.md`
