#!/usr/bin/env python3
"""
find-images.py — Multi-source image search for social posts.

Searches Unsplash + Pexels in parallel for a given category, downloads all
candidates to a dated folder, and opens an HTML preview where you can pick
the winner(s).

Usage:
    python3 ~/MDS/_sync/find-images.py "transport fleet"
    python3 ~/MDS/_sync/find-images.py "road train"
    python3 ~/MDS/_sync/find-images.py "plant hire"
    python3 ~/MDS/_sync/find-images.py            # interactive — lists categories

After review:
    Drag the keepers from _candidates/ into the dated _raw/ folder, or just
    use them directly with build-social-card.py — they're already on disk.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

CREDS = Path.home() / ".mds" / "credentials.json"
RAW_BASE = Path.home() / "MDS" / "tracknow-site" / "social-assets" / "_raw"
DEFAULT_CLIENT = "tracknow"  # passed as --client to override
RESULTS_PER_SOURCE = 6  # 6 from Unsplash + 6 from Pexels = 12 candidates

# Map shorthand category -> search query variants (we try the first that returns results).
# Edit this dictionary to add new categories.
CATEGORIES: dict[str, list[str]] = {
    "transport fleet":      ["truck fleet", "trucking", "freight trucks"],
    "road train":           ["road train", "long haul truck", "semi truck convoy"],
    "plant hire":           ["construction equipment", "excavator", "heavy machinery"],
    "civil construction":   ["construction site", "earthmoving", "excavator working"],
    "tradie vans":          ["tradesman van", "service van", "work vans construction"],
    "mining services":      ["mining equipment", "haul truck", "open pit mine"],
    "refrigerated transport":["refrigerated truck", "delivery truck", "freight truck"],
    "fleet manager":        ["fleet management", "logistics office", "dispatch"],
    "warehouse logistics":  ["warehouse logistics", "distribution warehouse", "forklift warehouse"],
    "highway truck":        ["semi truck highway", "trucks on road", "long haul truck"],
}


def load_creds() -> dict:
    if not CREDS.exists():
        sys.exit(f"Missing {CREDS} — set up credentials first")
    return json.loads(CREDS.read_text())


def http_get_json(url: str, headers: dict) -> dict:
    # Pexels (Cloudflare) rejects requests with no User-Agent. Always set one.
    headers = {**headers, "User-Agent": "find-images/1.0 (MDS internal tool)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def http_download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "find-images/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())


def search_unsplash(query: str, key: str, n: int) -> list[dict[str, Any]]:
    url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(query)}&per_page={n}&orientation=landscape"
    headers = {"Authorization": f"Client-ID {key}"}
    data = http_get_json(url, headers)
    return [
        {
            "source": "unsplash",
            "id": r["id"],
            "url_regular": r["urls"]["regular"],   # ~1080px
            "url_full": r["urls"]["full"],          # high-res
            "credit": f'{r["user"]["name"]} on Unsplash',
            "credit_url": r["user"]["links"]["html"],
            "ext": "jpg",
        }
        for r in data.get("results", [])
    ]


def search_pexels(query: str, key: str, n: int) -> list[dict[str, Any]]:
    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page={n}&orientation=landscape"
    headers = {"Authorization": key}
    data = http_get_json(url, headers)
    return [
        {
            "source": "pexels",
            "id": str(r["id"]),
            "url_regular": r["src"]["large"],       # ~1880x1253
            "url_full": r["src"]["original"],
            "credit": f'{r["photographer"]} on Pexels',
            "credit_url": r["photographer_url"],
            "ext": "jpg",
        }
        for r in data.get("photos", [])
    ]


def parallel_search(query: str, creds: dict, n: int) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    lock = threading.Lock()

    def runner(fn, *args):
        try:
            r = fn(*args)
            with lock:
                results.extend(r)
        except Exception as e:
            print(f"  ! {fn.__name__} failed: {e}")

    threads = [
        threading.Thread(target=runner, args=(search_unsplash, query, creds["unsplash_access_key"], n)),
        threading.Thread(target=runner, args=(search_pexels, query, creds["pexels_api_key"], n)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    return results


def download_all(items: list[dict[str, Any]], dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    threads = []
    for i, it in enumerate(items, 1):
        fname = f"{it['source']}-{i:02d}-{it['id']}.{it['ext']}"
        it["local_filename"] = fname
        dest = dest_dir / fname
        if dest.exists():
            continue

        def go(url=it["url_regular"], dest=dest):
            try:
                http_download(url, dest)
            except Exception as e:
                print(f"  ! download failed: {e}")

        t = threading.Thread(target=go)
        t.start()
        threads.append(t)
    for t in threads: t.join()


def write_preview(items: list[dict[str, Any]], category: str, query: str, out_dir: Path) -> Path:
    cards_html = ""
    for i, it in enumerate(items, 1):
        cards_html += f"""
        <div class="card">
          <img src="{it['local_filename']}" alt="{it['source']}-{it['id']}">
          <div class="meta">
            <div class="badge {it['source']}">{it['source'].upper()} #{i}</div>
            <div class="credit"><a href="{it['credit_url']}" target="_blank">{it['credit']}</a></div>
            <div class="filename">{it['local_filename']}</div>
            <a class="dl" href="{it['url_full']}" target="_blank">↧ full-res</a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>find-images: {category}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:14px/1.5 -apple-system,system-ui,sans-serif;background:#0f1932;color:#fff;padding:30px}}
h1{{font-size:26px;margin-bottom:6px}}
.lead{{color:#9aa5b8;margin-bottom:30px;font-size:14px}}
.lead code{{background:#1f2940;padding:2px 6px;border-radius:4px;color:#1ca2de}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:20px}}
.card{{background:#1f2940;border-radius:10px;overflow:hidden}}
.card img{{width:100%;display:block;cursor:zoom-in;aspect-ratio:16/10;object-fit:cover}}
.card img.zoomed{{aspect-ratio:auto;cursor:zoom-out}}
.meta{{padding:12px 14px}}
.badge{{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:600;letter-spacing:0.5px}}
.badge.unsplash{{background:#000;color:#fff}}
.badge.pexels{{background:#05a081;color:#fff}}
.credit{{margin-top:8px;color:#9aa5b8;font-size:12px}}
.credit a{{color:#9aa5b8;text-decoration:none}}
.credit a:hover{{color:#1ca2de}}
.filename{{margin-top:6px;color:#5a6480;font-size:11px;font-family:ui-monospace,monospace}}
.dl{{display:inline-block;margin-top:10px;color:#1ca2de;text-decoration:none;font-size:12px}}
.dl:hover{{text-decoration:underline}}
</style>
<script>
document.addEventListener('click', e => {{
  if (e.target.tagName === 'IMG' && e.target.closest('.card')) e.target.classList.toggle('zoomed');
}});
</script>
</head><body>
<h1>{category}</h1>
<p class="lead">Search query: <code>{query}</code> &nbsp;·&nbsp; {len(items)} results &nbsp;·&nbsp; folder: <code>{out_dir}</code></p>
<p class="lead"><strong>Pick:</strong> Click any image to zoom. To use one — drag from the candidates folder into <code>_raw/YYYY-MM-DD/</code>, or pass the local path directly to <code>build-social-card.py</code>.</p>
<div class="grid">{cards_html}</div>
</body></html>"""

    preview = out_dir / "preview.html"
    preview.write_text(html)
    return preview


def main() -> None:
    creds = load_creds()
    if "unsplash_access_key" not in creds or "pexels_api_key" not in creds:
        sys.exit("Missing unsplash_access_key or pexels_api_key in ~/.mds/credentials.json")

    # --client <slug> overrides the default client folder (otherwise tracknow)
    args = sys.argv[1:]
    client = DEFAULT_CLIENT
    if "--client" in args:
        i = args.index("--client")
        client = args[i + 1]
        args = args[:i] + args[i + 2:]

    if not args:
        print("Usage:  find-images.py \"<category or freeform query>\" [--client <slug>]")
        print(f"\nDefault client: {DEFAULT_CLIENT}")
        print("\nPredefined categories:")
        for c in CATEGORIES:
            print(f"  • {c}")
        print("\nFreeform also works — anything else is sent to both APIs as-is.")
        sys.exit(0)

    user_input = " ".join(args).strip().lower()
    queries = CATEGORIES.get(user_input, [user_input])

    # Try first query; if it returns nothing, try next.
    results: list[dict[str, Any]] = []
    chosen_query = queries[0]
    for q in queries:
        print(f"Searching: {q!r} ...")
        results = parallel_search(q, creds, RESULTS_PER_SOURCE)
        if results:
            chosen_query = q
            break

    if not results:
        sys.exit("No results from any source. Try a different query.")

    print(f"Got {len(results)} results from {len(set(r['source'] for r in results))} sources.")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_cat = user_input.replace(" ", "-").replace("/", "-")
    out_dir = RAW_BASE / "_candidates" / client / f"{timestamp}_{safe_cat}"
    print(f"Client: {client}")
    print(f"Downloading to {out_dir} ...")
    download_all(results, out_dir)

    preview = write_preview(results, user_input, chosen_query, out_dir)
    print(f"\nPreview: {preview}")
    subprocess.Popen(["open", "-a", "Google Chrome", str(preview)])


if __name__ == "__main__":
    main()
