#!/usr/bin/env python3
"""
TrackNow daily post monitor.

Runs at 6pm AEST every weekday via LaunchAgent. Queries social-hub for posts
scheduled today, checks each status, posts a macOS notification with the
end-of-day summary, and logs the result.

Posts are flagged as problems if status is one of:
  - failed (Buffer rejected the post)
  - awaiting_approval (Mark didn't click the magic link in time)
  - pending (James didn't click "Send for approval" in admin)

Otherwise a clean summary is shown ("5/5 posted ✅").

Manual run:
  python3 ~/MDS/mds-diversified/scripts/tracknow-post-monitor.py
"""
from __future__ import annotations

import json
import subprocess
import urllib.request
from datetime import date, datetime
from pathlib import Path

HUB = "https://mds-social-hub.onrender.com"
LOG = Path.home() / "MDS" / ".logs" / "tracknow-post-monitor.log"
CREDS = Path.home() / ".mds" / "credentials.json"
PROBLEM_STATUSES = {"failed", "awaiting_approval", "pending"}


def load_key() -> str:
    return json.loads(CREDS.read_text())["hub_api_key"]


def fetch_posts(key: str) -> list[dict]:
    """Try /api/posts (full list) — fall back to per-id fetches if that route doesn't exist."""
    headers = {"Authorization": f"Bearer {key}"}
    # /api/clients first to confirm tracknow exists
    req = urllib.request.Request(f"{HUB}/api/clients", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        clients = json.loads(r.read().decode())
    tracknow = next((c for c in clients if c.get("slug") == "tracknow"), None)
    if not tracknow:
        return []
    # Iterate post IDs — social-hub API doesn't currently expose a "list all" route
    # but /api/posts/{id} works. We sweep a recent ID range backward until we hit
    # consecutive 404s, then stop.
    posts: list[dict] = []
    miss_streak = 0
    pid = 100  # safe upper bound — extend if needed
    while pid > 0 and miss_streak < 10:
        req = urllib.request.Request(f"{HUB}/api/posts/{pid}", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                p = json.loads(r.read().decode())
                posts.append(p)
                miss_streak = 0
        except urllib.error.HTTPError as e:
            if e.code == 404:
                miss_streak += 1
            else:
                break
        pid -= 1
    return posts


def today_posts_for_tracknow(posts: list[dict]) -> list[dict]:
    today_str = date.today().isoformat()
    return [p for p in posts if p.get("scheduled_at", "").startswith(today_str)
            or p.get("scheduled_at", "")[:10] == today_str]


def summarise(posts_today: list[dict]) -> tuple[str, str]:
    """Return (title, body) for the macOS notification."""
    if not posts_today:
        return ("TrackNow monitor", f"No posts scheduled for {date.today().isoformat()}.")
    n = len(posts_today)
    by_status: dict[str, list[int]] = {}
    for p in posts_today:
        by_status.setdefault(p.get("status", "?"), []).append(p["id"])
    posted = len(by_status.get("posted", []))
    problems = {s: ids for s, ids in by_status.items() if s in PROBLEM_STATUSES}
    if posted == n:
        return ("TrackNow ✅", f"{posted}/{n} posted today")
    if not problems:
        non_terminal = [(s, ids) for s, ids in by_status.items() if s not in {"posted"}]
        line = ", ".join(f"{s} ({len(ids)})" for s, ids in non_terminal)
        return ("TrackNow — in progress", f"{posted}/{n} posted · {line}")
    flag = ", ".join(f"{s}: ids {ids}" for s, ids in problems.items())
    return ("TrackNow ⚠️ issues", f"{posted}/{n} posted · {flag}")


def notify(title: str, body: str) -> None:
    """macOS native notification."""
    safe = body.replace('"', "'")
    subprocess.run(
        [
            "osascript",
            "-e",
            f'display notification "{safe}" with title "{title}"',
        ],
        check=False,
    )


def log(line: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {line}\n")


def main() -> None:
    try:
        key = load_key()
    except Exception as e:
        notify("TrackNow monitor — error", f"Could not load API key: {e}")
        log(f"FATAL load_key: {e}")
        return
    try:
        posts = fetch_posts(key)
    except Exception as e:
        notify("TrackNow monitor — error", f"social-hub API: {e}")
        log(f"FATAL fetch_posts: {e}")
        return
    today = today_posts_for_tracknow(posts)
    title, body = summarise(today)
    notify(title, body)
    log(f"{title} | {body}")


if __name__ == "__main__":
    # Top-level failure alert: any unexpected crash (e.g. a malformed post,
    # osascript missing, a code bug) still surfaces a notification + log line
    # instead of dying silently and leaving James thinking the monitor ran.
    try:
        main()
    except Exception as e:  # noqa: BLE001 — last-resort catch-all is the point
        import traceback

        try:
            notify("TrackNow monitor — crashed", f"{type(e).__name__}: {e}")
        except Exception:
            pass
        try:
            log(f"CRASH {type(e).__name__}: {e}\n{traceback.format_exc()}")
        except Exception:
            pass
        raise
