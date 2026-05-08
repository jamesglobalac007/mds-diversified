# Image-picking workflow — repeatable process

The single image step before every TrackNow post. ~30 sec to 2 min depending on whether stock delivers.

## Steps

### 1. Decide the scene in plain English
Examples: `"transport fleet"`, `"plant hire yard"`, `"tradie van site"`, `"road train sunset"`, `"refrigerated truck"`.

### 2. Run stock search (5 sec, free)
```bash
python3 ~/MDS/_sync/find-images.py "<category>"
```
Preview opens in browser with 12 candidates from Unsplash + Pexels.

### 3. Pick the winner from stock — OR decide none work
- Click any image to zoom
- If one's perfect → grab it (step 4a)
- If none hit → fall back to AI (step 4b)

### 4a. Stock winner found
Drag the winning file from the candidates folder
(`~/MDS/tracknow-site/social-assets/_raw/_candidates/<timestamp>_<category>/`)
into the dated batch folder
(`~/MDS/tracknow-site/social-assets/_raw/<client>/YYYY-MM-DD/`).

Rename to something descriptive like `transport-fleet-depot.jpg`.

### 4b. None of the stock works → use AI
- Open https://gemini.google.com (free, covered by your Google AI Pro / Flow sub)
- Type a descriptive prompt:
  > "Photorealistic Australian truck depot at golden hour. Right-hand drive Kenworth prime movers, eucalyptus trees, hi-vis worker, no readable text or signage. Wide-angle aerial."
- Generate
- **Drag the image directly from Gemini into the Finder window** for the dated batch folder
  *(no need to "Save" first — drag from browser → Finder works)*
- Rename to something descriptive

### 5. Done
Image is on disk in `~/MDS/tracknow-site/social-assets/_raw/<client>/YYYY-MM-DD/<descriptive-name>.png`.

Ready for the next stage (branding card → caption → push to social-hub).

---

## Tips for AI prompt quality (when using Gemini)

Always include in the prompt:
- **"Australian"** or **"Aussie"** — without it you get American trucks/scenes
- **"Right-hand drive"** if vehicles are featured — fixes the wrong-side steering issue
- **"No readable text or signage"** — kills the AI gibberish-text problem
- **"Photorealistic, golden hour"** — gets cinematic warmth
- Specify what's in the foreground, mid-ground, background — gives AI structure

### Categories that need an "Aussie" prompt addition

| Generic prompt | Add this Aussie cue |
|----------------|---------------------|
| Truck depot | "Eucalyptus trees, Australian flag truck markings" |
| Plant hire | "Outer-suburb industrial estate" |
| Road train | "Outback red dirt, Stuart Highway, NT plate" |
| Civil construction | "Australian residential build, brick veneer" |
| Tradie vans | "Australian tradies, hi-vis with Aussie work boots" |

---

## Tools reference

- **Stock search:** `~/MDS/_sync/find-images.py "<category>" [--client <slug>]`
  - Default client: `tracknow` — pass `--client <slug>` to override
- **Credentials:** `~/.mds/credentials.json` (Unsplash + Pexels keys, plus Gemini API for future automation)
- **Categories config:** edit `CATEGORIES` dict in `find-images.py` to add new presets
- **Output folder:** `~/MDS/tracknow-site/social-assets/_raw/<client>/YYYY-MM-DD/`
- **Candidates from search:** `~/MDS/tracknow-site/social-assets/_raw/_candidates/<client>/`

## Adding a new client

1. Create the client folder + 30 future dated subfolders:
   ```bash
   python3 -c "
   from pathlib import Path; from datetime import date, timedelta
   base = Path.home()/'MDS'/'tracknow-site'/'social-assets'/'_raw'/'NEWCLIENT'
   for i in range(32):
       (base / (date.today() + timedelta(days=i)).isoformat()).mkdir(parents=True, exist_ok=True)
   "
   ```
2. Run searches with the override flag:
   `python3 ~/MDS/_sync/find-images.py "transport fleet" --client newclient`
3. Add client-specific categories to `CATEGORIES` in `find-images.py` if the defaults don't fit.
