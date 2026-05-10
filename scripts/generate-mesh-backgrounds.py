"""
Generate gradient-mesh background images for the MDS Diversified site.

Each image is 1920x1080, built from soft radial gradient blobs that match the
brand palette in ~/MDS/mds-diversified/admin/mds-brand-identity.md, then
finished with a subtle grain/noise pass for premium texture.

These sit under heavy CSS overlays (86-96% opacity) on the live site, so the
mesh is texture rather than illustration.

Run from project root:
    python3 scripts/generate-mesh-backgrounds.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
OUT = Path(__file__).resolve().parent.parent / "assets" / "images"

# MDS palette (hex -> RGB)
P = {
    "indigo":     (94,  92,  230),
    "blue":       (10,  132, 255),
    "cobalt":     (29,  63,  255),
    "cyan":       (50,  173, 230),
    "teal":       (48,  213, 200),
    "green":      (30,  215, 96),
    "green_deep": (13,  79,  44),
    "amber":      (255, 159, 10),
    "orange":     (255, 107, 53),
    "pink":       (255, 45,  146),
    "magenta":    (194, 24,  91),
    "purple":     (191, 90,  242),
    "ink":        (12,  13,  16),
    "paper":      (255, 255, 255),
}


def make_blob(canvas: np.ndarray, cx: float, cy: float, rx: float, ry: float,
              colour: tuple[int, int, int], strength: float) -> None:
    """Paint one soft radial gradient blob using alpha compositing.

    Works correctly regardless of base colour: on white the blob darkens toward
    its hue, on black it brightens toward its hue, on a mid base it shifts
    toward its hue.
    """
    h, w, _ = canvas.shape
    y, x = np.ogrid[:h, :w]
    dx = (x - cx) / rx
    dy = (y - cy) / ry
    r2 = dx * dx + dy * dy
    alpha = np.exp(-r2 * 1.7).astype(np.float32) * strength
    alpha = np.clip(alpha, 0.0, 1.0)[..., None]  # HxWx1
    blob_rgb = np.array(colour, dtype=np.float32).reshape(1, 1, 3)
    canvas[...] = (1.0 - alpha) * canvas + alpha * blob_rgb


def render(blobs: list[tuple], base: tuple[int, int, int], grain: float = 8.0,
           blur_radius: float = 0.0) -> Image.Image:
    """Render an image from a list of blobs on top of a base colour."""
    canvas = np.zeros((H, W, 3), dtype=np.float32)
    canvas[..., 0] = base[0]
    canvas[..., 1] = base[1]
    canvas[..., 2] = base[2]

    for cx, cy, rx, ry, colour, strength in blobs:
        make_blob(canvas, cx, cy, rx, ry, colour, strength)

    # Grain noise (subtle, monochrome, gaussian)
    if grain > 0:
        rng = np.random.default_rng(seed=42)
        noise = rng.normal(0.0, grain, (H, W, 1)).astype(np.float32)
        canvas += noise

    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    img = Image.fromarray(canvas, "RGB")

    if blur_radius > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    return img


# ---------- Per-image specs ----------

def hero() -> Image.Image:
    """Full aurora — indigo/cyan/green/amber across the whole canvas.
    Sits under a 92-96% white overlay, so blobs need real saturation to come
    through after the wash."""
    return render(
        base=P["paper"],
        blobs=[
            (W * 0.12, H * 0.18, 720, 620, P["indigo"], 0.45),
            (W * 0.88, H * 0.22, 680, 560, P["cyan"],   0.45),
            (W * 0.80, H * 0.88, 660, 540, P["green"],  0.42),
            (W * 0.14, H * 0.92, 600, 500, P["amber"],  0.32),
            (W * 0.50, H * 0.50, 900, 720, P["teal"],   0.15),
        ],
        grain=4.0,
    )


def always_on() -> Image.Image:
    """Cool deep — indigo + blue + teal + a green pulse on a near-black base."""
    return render(
        base=P["ink"],
        blobs=[
            (W * 0.18, H * 0.28, 760, 620, P["blue"],   0.85),
            (W * 0.82, H * 0.72, 700, 580, P["teal"],   0.75),
            (W * 0.50, H * 0.95, 620, 520, P["green"],  0.60),
            (W * 0.92, H * 0.08, 580, 480, P["amber"],  0.45),
            (W * 0.10, H * 0.85, 520, 440, P["indigo"], 0.55),
        ],
        grain=10.0,
    )


def get_started() -> Image.Image:
    """Warm launch — amber→orange→pink trajectory across white.
    Used under a light overlay; mid-saturation so it doesn't blow out."""
    return render(
        base=P["paper"],
        blobs=[
            (W * 0.15, H * 0.85, 720, 600, P["amber"],   0.42),
            (W * 0.50, H * 0.50, 820, 660, P["orange"],  0.35),
            (W * 0.85, H * 0.15, 700, 580, P["pink"],    0.40),
            (W * 0.30, H * 0.20, 540, 460, P["purple"],  0.25),
        ],
        grain=4.0,
    )


def marketing() -> Image.Image:
    """grad-primary territory — indigo→blue→cyan only. No warm tones."""
    return render(
        base=P["ink"],
        blobs=[
            (W * 0.18, H * 0.25, 780, 640, P["indigo"], 0.95),
            (W * 0.82, H * 0.75, 720, 600, P["cyan"],   0.85),
            (W * 0.60, H * 0.35, 680, 560, P["blue"],   0.75),
            (W * 0.35, H * 0.80, 540, 460, P["teal"],   0.55),
        ],
        grain=10.0,
    )


def sales_relay() -> Image.Image:
    """grad-warm territory — amber→orange→pink→purple."""
    return render(
        base=P["ink"],
        blobs=[
            (W * 0.82, H * 0.25, 780, 640, P["pink"],    0.95),
            (W * 0.18, H * 0.75, 720, 600, P["amber"],   0.75),
            (W * 0.50, H * 0.45, 700, 580, P["orange"],  0.70),
            (W * 0.65, H * 0.85, 540, 460, P["purple"],  0.55),
        ],
        grain=10.0,
    )


SPECS = {
    "hero.jpg": hero,
    "always-on.jpg": always_on,
    "get-started.jpg": get_started,
    "marketing.jpg": marketing,
    "sales-relay.jpg": sales_relay,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SPECS.items():
        path = OUT / name
        img = fn()
        img.save(path, "JPEG", quality=88, optimize=True)
        print(f"wrote {path.relative_to(OUT.parent.parent)} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
