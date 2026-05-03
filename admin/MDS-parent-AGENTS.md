# MDS Codex Instructions

This file is the parent-folder entry point for Codex when started from `~/MDS/`. All MDS client and internal projects live under `~/MDS/`.

## Path Rules

James works from two Macs. Always use `~/MDS/` in commands so paths resolve on both machines.

| Machine | Username | Path |
|---|---|---|
| Mac mini work machine | `jamesglobal` | `~/MDS/` |
| Mac laptop home machine | `tiffanydrake` | `~/MDS/` |

Never reference, create, or suggest project files outside `~/MDS/`. Do not use `~/Dropbox/`, `~/Desktop/`, `~/Documents/`, `~/Downloads/`, iCloud, or temporary transfer folders for MDS work.

If the exact project folder is not known, ask James. Do not guess.

## Project Registry

Before acting, resolve the project from this registry, from `~/MDS/CLAUDE.md`, or from the current `AGENTS.md`. Then change into the project folder and read that project's own `AGENTS.md` or `CLAUDE.md` if present.

| User wording | Project slug | Local folder | GitHub repo | Live URL |
|---|---|---|---|---|
| "mds diversified", "mds live link" | `mds-diversified` | `~/MDS/mds-diversified/` | `jamesglobalac007/mds-diversified` | https://mds-diversified.onrender.com |
| "conversations" | `conversations` | `~/MDS/conversations/` | `jamesglobalac007/mds-conversations` | none |
| "deal vault" | `deal-vault` | `~/MDS/deal-vault/` | `jamesglobalac007/deal-vault` | https://deal-vault.onrender.com |
| "LC AI", "LC AI portal" | `LC-AI-Portal` | `~/MDS/LC-AI-Portal/` | `jamesglobalac007/LC-AI-Portal` | https://lc-ai-portal.onrender.com |
| "manson invest" | `Manson--Invest` | `~/MDS/Manson--Invest/` | `jamesglobalac007/Manson--Invest` | https://manson-invest.onrender.com |
| "radius", "NDIS", "SDA" | `radius-ndis-sda-platform` | `~/MDS/radius-ndis-sda-platform/` | `jamesglobalac007/radius-ndis-sda-platform` | https://radius-ndis-sda-platform.onrender.com |
| "sb", "s&b empire", "sb empire portal" | `sb-empire-portal` | `~/MDS/sb-empire-portal/` | `jamesglobalac007/sb-empire-portal` | https://sb-empire-portal.onrender.com |
| "sbp sandbox", "sb empire test", "sb empire sandbox" | `sandbox-sb-empire` | `~/MDS/sandbox-sb-empire/` | `jamesglobalac007/sandbox-sb-empire` | https://sandbox-sb-empire.onrender.com |
| "mds invoices", "invoice portal", "mds billing" | `mds-invoices` | `~/MDS/mds-invoices/` | `jamesglobalac007/mds-invoices` | pending Render deploy |
| "mds content", "content library", "client content", "social profiles", "profile pics" | `mds-content` | `~/MDS/mds-content/` | `jamesglobalac007/mds-content` | none |
| "tracknow site", "tracknow website", "website" | `tracknow-site` | `~/MDS/tracknow-site/` | `jamesglobalac007/tracknow-site` | https://tracknow-site.onrender.com |
| "tracknow portal", "portal", "dashboard", "client login" | `tracknow-portal` | `~/MDS/tracknow-portal/` | `jamesglobalac007/tracknow-portal` | https://tracknow-portal.onrender.com |
| "tracknow sandbox", "tracknow test", "sandbox tracknow" | `sandbox-tracknow` | `~/MDS/sandbox-tracknow/` | `jamesglobalac007/sandbox-tracknow` | https://sandbox-tracknow.onrender.com |
| "tracknow portal sync" | `tracknow-portal-sync` | no local folder | n/a | https://tracknow-portal-sync.onrender.com |

## TrackNow Distinction

TrackNow has two separate projects:

- `tracknow-site`: public marketing website, demo, hardware page, hero video, HVNL/CoR content, and sector positioning.
- `tracknow-portal`: customer portal, login, dashboard, sales portal, proposals, and client data.

If James says "TrackNow site" or "website", use `~/MDS/tracknow-site/`.
If James says "TrackNow portal", "portal", "dashboard", or "client login", use `~/MDS/tracknow-portal/`.
If James only says "TrackNow", ask which one before editing, deploying, or pushing.

## Ask Versus Act

Check local files first. If the answer is discoverable from the repo, inspect the repo and proceed.

Ask James only when proceeding could affect the wrong project, wrong client, wrong live system, sensitive data, billing, credentials, or an irreversible action. For low-risk choices, make a reasonable decision and explain it briefly.

Do not repeatedly apologize. Do not repeatedly say "I won't assume" when the answer can be found locally. Use judgement, verify from files, and move the work forward.

## Simplicity and Time Rule

James values simplicity, consistency, and time management over clever or complex systems.

- Default to the simplest reliable workflow: 1 + 1 = 2.
- Keep files, folders, approvals, and automations in predictable places.
- Avoid adding tools, steps, dashboards, abstractions, or integrations unless they clearly save time.
- Prefer one source of truth, one approval path, and one clean handoff.
- If a workflow starts creating extra admin, simplify it before scaling it.
- Explain the chosen flow briefly in plain language so James can trust and repeat it.

## Client Content Workflow

When creating marketing content for a known client, use both systems:

- Save the content source files under `~/MDS/mds-content/clients/<client-slug>/`.
- Update the relevant Google Sheet approval/scheduling workflow with the useful path or share link.
- For normal posts, use `posts/drafts/`, then move to `approved/`, `scheduled/`, or `published/` as the work progresses.
- For videos, use `videos/drafts/` and the matching status folders.
- For social profile work, including profile pictures, cover images, bios, and platform setup notes, use `social-profiles/`.
- For profile pictures specifically, use `social-profiles/profile-pictures/`.

Local Mac file paths are for internal tracking only. If the client, Make, Metricool, or a Google Sheet needs to open an asset, also create or use a shareable Google Drive/hosted link.

## GitHub Sync Workflow

GitHub is the source of truth between the Mac mini and Mac laptop.

- Pull before work where appropriate, especially before larger edits or when the repo may have changed on the other machine.
- Commit and push after meaningful approved changes unless James explicitly says not to.
- Use specific `git add` paths. Do not use blanket adds for noisy working trees.
- Write commit messages that explain why the change was made.
- Push to the current branch, usually `main`.
- Never commit secrets, API keys, passwords, private customer exports, or encryption keys.
- If a push fails, say so plainly and leave the repo state clear.
- At the end of a session, check `git status` in every MDS repo touched and resolve any uncommitted or unpushed work.

## Backup Repo Rules

Backup repos are for encrypted, auto-populated restore snapshots. Do not hand-edit backup contents unless James specifically asks for a recovery or maintenance task.

Known backup repos:

| Backup repo | Local folder | GitHub repo | Source project |
|---|---|---|---|
| TrackNow portal backups | `~/MDS/tracknow-portal-backups/` | `jamesglobalac007/tracknow-portal-backups` | `tracknow-portal` |
| S&B Empire portal backups | `~/MDS/sb-empire-portal-backups/` | `jamesglobalac007/sb-empire-portal-backups` | `sb-empire-portal` |

Backup snapshots are encrypted. The encryption key must never be committed, printed into logs, pasted into files, or pushed to GitHub. If restoring data, read the backup repo README first and treat restored JSON as sensitive customer data.

## Common References

- GitHub username: `jamesglobalac007`
- James email: `james@mdsdiversified.ai`
- Domain not yet connected to Render: `mdsdiversified.ai`
- Canonical parent Claude source: `~/MDS/mds-diversified/admin/MDS-parent-CLAUDE.md`
- Canonical parent Codex source: `~/MDS/mds-diversified/admin/MDS-parent-AGENTS.md`
