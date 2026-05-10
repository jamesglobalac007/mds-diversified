# MDS Diversified — Brand Identity

Canonical brand reference for MDS Diversified (the parent firm). Used by the `brand`, `design`, `frontend-design`, and `ui-ux-pro-max` skills when designing or reviewing any MDS Diversified surface.

> **Per-client brands** (TrackNow, S&B Empire, LC AI, Manson, Radius, Conversations, Deal Vault) live in each project's own `CLAUDE.md`. This file is **only** the parent MDS Diversified identity.

---

## 1. Color palette

Source of truth: `~/MDS/mds-diversified/assets/site.css` (`:root` block).

### Neutrals
| Token | Hex | Usage |
|-------|-----|-------|
| `--ink` | `#0c0d10` | Body text, primary headings on light bg |
| `--ink-soft` | `#2a2c33` | Secondary text on light bg |
| `--muted` | `#6e6e73` | Captions, helper text |
| `--line` | `#e5e5ea` | Dividers, borders |
| `--paper` | `#ffffff` | Default page background |
| `--soft` | `#f5f5f7` | Section backgrounds, cards |

### Vibrant accents (use sparingly, almost always inside a gradient)
| Token | Hex | Note |
|-------|-----|------|
| `--indigo` | `#5e5ce6` | Primary cool anchor |
| `--blue` | `#0a84ff` | Apple-blue, CTAs |
| `--cobalt` | `#1d3fff` | Deep cool accent |
| `--cyan` | `#32ade6` | Cool gradient stop |
| `--teal` | `#30d5c8` | Fresh accent |
| `--green` | `#1ed760` | Spotify lime — "convert", "yes", momentum |
| `--green-deep` | `#0d4f2c` | Deep accent for subtle backgrounds |
| `--amber` | `#ff9f0a` | Warm anchor |
| `--orange` | `#ff6b35` | Warm gradient mid |
| `--pink` | `#ff2d92` | Energy accent |
| `--magenta` | `#c2185b` | Deep warm |
| `--purple` | `#bf5af2` | Aurora gradient stop |

### Signature gradients (use these — don't reinvent)
- `--grad-primary` — indigo → blue → cyan (135deg). Default cool gradient.
- `--grad-warm` — amber → orange → pink → purple (135deg). Warm/energy gradient.
- `--grad-aurora` — indigo → purple → pink (135deg). Hero "wow" gradient.

### Hero ambient background
Stacked radial gradients on a white base, subtle drift animation. See `.hero-section::before` in `site.css` — lift this pattern, do not invent new ones.

---

## 2. Typography

### Font stack
```css
font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```
Inter only. No serif, no display fonts. System fallback is acceptable.

### Scale (from live site)
| Element | Weight | Size | Line height | Letter-spacing |
|---------|--------|------|-------------|----------------|
| Hero h1 | 800 | `clamp(3rem, 9vw, 8rem)` | 0.94 | -0.04em |
| Section h2 | 800 | `clamp(2rem, 4vw, 3.7rem)` | 1.04 | 0 |
| Marquee | 800 | `clamp(2.4rem, 6vw, 5.4rem)` | — | -0.025em |
| Big number | 900 | — | 0.82 | -0.05em |
| Subtitle | 400 | `clamp(1.15rem, 1.85vw, 1.55rem)` | 1.45 | — |
| Body | 400 | 16px | 1.55 | — |
| Eyebrow | 800 | 0.78rem | — | 0.18em (uppercase) |
| Nav | 700 | 0.92rem | — | — |
| Button | 750 | 1rem | — | — |

**Rule:** headings get tight, negative letter-spacing and heavy weight. Body stays neutral and readable. Eyebrow uses uppercase with wide tracking.

---

## 3. Voice

Three traits: **sales-led, action-focused, anti-fluff.**

Hero copy on live site:
- *"Sales and marketing, built around action."* (eyebrow)
- *"Marketing that attracts. Sales that convert."* (h1, with key verbs in gradient)
- *"Better sales conversations. Sharper marketing. Faster follow-up."* (subtitle)

### Patterns to keep
- Short declarative sentences. Period at the end of each. Three-beat rhythm: *"Less noise. More work that supports revenue."*
- Verbs do the work. Highlight the verb in gradient (`<span class="grad-text grad-blue">attracts</span>`), not the noun.
- "And" pairings to balance the two sides: sales **and** marketing, find **and** improve, plan **and** support.
- Questions where they punch: *"Are you in?"*, *"Ready to generate new business?"*

### Patterns to avoid
- No emojis anywhere — UI labels, copy, modals, disclaimers, my own responses to James. (See feedback memory `feedback_no_emojis.md`.)
- No agency-speak: "synergy", "leverage", "ecosystem", "solution".
- No fluff modifiers: "truly", "really", "very", "incredibly".
- No exclamation marks.
- No corporate hedging: "we believe", "we feel", "it's our hope that".

---

## 4. Layout & motion

- **Background = white.** Color comes from gradients and accents, not fields of color.
- **Generous vertical rhythm.** `clamp()` for spacing too — never fixed pixels for hero/section padding.
- **Centered hero, left-aligned scenes.** Hero is grid-centered with `justify-items: center`. Below the fold, sections shift to grid + left alignment.
- **Subtle motion only.** `hero-drift` 22s ease-in-out alternate, `marquee` 28s linear infinite. No bouncing, no parallax, no scroll-jacking.
- **Shadow:** `--shadow: 0 18px 50px rgba(0, 0, 0, 0.08)` — soft, far, low opacity. Don't invent harder shadows.

---

## 5. Logo

Lives in `~/MDS/mds-diversified/assets/`. Header treatment: 280px wide, max 90px tall, `object-fit: contain`. Header background `#050510` (near-black, not pure black) with a 1px translucent white border.

---

## 6. When designing a NEW MDS Diversified surface

Default checklist:
1. Inter font, white background, ink text.
2. Use one signature gradient (`--grad-primary`, `--grad-warm`, or `--grad-aurora`) — pick based on tone, don't mix two on the same surface.
3. Highlight verbs (not nouns) with gradient text.
4. Tight negative letter-spacing on headings.
5. Eyebrow → h1 → subtitle structure for hero, with ~10px gap between h1 and subtitle.
6. No emojis. Three-beat declarative sentences for body copy.
7. CTA = pill button, white background on dark / dark on white, hover shifts to `--green`.

If a request would break any of the above, flag it before doing it.
