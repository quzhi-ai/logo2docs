#!/usr/bin/env python3
"""
Brand Setup — Extract colors from a logo and generate a complete brand-config.json.

Usage:
  python brand_setup.py extract-colors --image logo.png
  python brand_setup.py generate-config --primary "#045e81" --secondary "#15a04a" --style modern --industry logistics --output brand-config.json
  python brand_setup.py embed-logo --color logo-color.png [--white logo-white.png] --config brand-config.json
"""

import argparse
import base64
import colorsys
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color utilities
# ---------------------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def hsl_to_rgb(h, s, l):
    h, s, l = h / 360.0, s / 100.0, l / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def adjust_lightness(hex_color, target_lightness):
    r, g, b = hex_to_rgb(hex_color)
    h, s, _ = rgb_to_hsl(r, g, b)
    nr, ng, nb = hsl_to_rgb(h, s, target_lightness)
    return rgb_to_hex(nr, ng, nb)


def luminance(r, g, b):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(hex1, hex2):
    l1 = luminance(*hex_to_rgb(hex1))
    l2 = luminance(*hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def is_near_white(r, g, b, threshold=240):
    return r > threshold and g > threshold and b > threshold


def is_near_black(r, g, b, threshold=15):
    return r < threshold and g < threshold and b < threshold


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


# ---------------------------------------------------------------------------
# extract-colors command
# ---------------------------------------------------------------------------

def extract_colors(image_path, top_n=5):
    img = Image.open(image_path).convert("RGBA")

    width, height = img.size
    aspect_ratio = round(width / height, 4)

    img_small = img.resize((150, 150), Image.LANCZOS)

    pixels = []
    get_data = getattr(img_small, "get_flattened_data", img_small.getdata)
    for pixel in get_data():
        r, g, b, a = pixel
        if a < 128:
            continue
        if is_near_white(r, g, b) or is_near_black(r, g, b):
            continue
        quantized = (r // 16 * 16, g // 16 * 16, b // 16 * 16)
        pixels.append(quantized)

    if not pixels:
        print("WARNING: No significant colors found. Logo may be monochrome or transparent.", file=sys.stderr)
        return {"colors": [], "aspect_ratio": aspect_ratio}

    counter = Counter(pixels)
    total = len(pixels)

    merged = []
    for color, count in counter.most_common(50):
        found_cluster = False
        for i, (c, cnt) in enumerate(merged):
            if color_distance(color, c) < 40:
                if count > cnt:
                    merged[i] = (color, cnt + count)
                else:
                    merged[i] = (c, cnt + count)
                found_cluster = True
                break
        if not found_cluster:
            merged.append((color, count))

    merged.sort(key=lambda x: x[1], reverse=True)

    results = []
    for color, count in merged[:top_n]:
        hex_val = rgb_to_hex(*color)
        pct = round(count / total * 100, 1)
        results.append({"hex": hex_val, "rgb": list(color), "percentage": pct})

    output = {
        "colors": results,
        "aspect_ratio": aspect_ratio,
        "image_size": {"width": width, "height": height}
    }

    print(json.dumps(output, indent=2))
    return output


# ---------------------------------------------------------------------------
# generate-config command
# ---------------------------------------------------------------------------

FONT_PRESETS = {
    "professional": {
        "heading": {"family_web": "Georgia, 'Times New Roman', serif", "family_office": "Georgia", "weight": 700},
        "body": {"family_web": "'Noto Sans', 'Segoe UI', sans-serif", "family_office": "Calibri", "weight": 400},
    },
    "modern": {
        "heading": {"family_web": "Manrope, 'Inter', sans-serif", "family_office": "Calibri", "weight": 700},
        "body": {"family_web": "'Noto Sans SC', 'Segoe UI', sans-serif", "family_office": "Calibri", "weight": 400},
    },
    "bold": {
        "heading": {"family_web": "'Montserrat', 'Arial Black', sans-serif", "family_office": "Arial Black", "weight": 800},
        "body": {"family_web": "'Noto Sans', 'Segoe UI', sans-serif", "family_office": "Calibri", "weight": 400},
    },
    "elegant": {
        "heading": {"family_web": "'Playfair Display', Georgia, serif", "family_office": "Georgia", "weight": 600},
        "body": {"family_web": "'Source Sans Pro', 'Segoe UI', sans-serif", "family_office": "Calibri Light", "weight": 300},
    },
}


def generate_chart_series(primary_hex, secondary_hex, count=6):
    """Generate a harmonious chart color series from primary and secondary."""
    r1, g1, b1 = hex_to_rgb(primary_hex)
    h1, s1, l1 = rgb_to_hsl(r1, g1, b1)

    r2, g2, b2 = hex_to_rgb(secondary_hex)
    h2, s2, l2 = rgb_to_hsl(r2, g2, b2)

    series = [primary_hex, secondary_hex]

    hue_step = 360 / (count + 1)
    base_hues = [(h1 + hue_step * (i + 1)) % 360 for i in range(count - 2)]

    for hue in base_hues:
        avg_s = (s1 + s2) / 2
        r, g, b = hsl_to_rgb(hue, min(avg_s, 75), 45)
        series.append(rgb_to_hex(r, g, b))

    return series[:count]


def find_safe_text_color(bg_hex):
    """Find a text color that meets WCAG AA contrast (4.5:1) against the background."""
    candidates = ["#ffffff", "#f7fafc", "#e2e8f0", "#1a202c", "#2d3748", "#000000"]
    for c in candidates:
        if contrast_ratio(bg_hex, c) >= 4.5:
            return c
    cr_white = contrast_ratio(bg_hex, "#ffffff")
    cr_dark = contrast_ratio(bg_hex, "#000000")
    return "#ffffff" if cr_white > cr_dark else "#000000"


def generate_config(primary, secondary, style="modern", industry="general", company_name="", output_path="brand-config.json"):
    style = style.lower() if style else "modern"
    if style not in FONT_PRESETS:
        style = "modern"

    fonts = FONT_PRESETS[style]

    pr, pg, pb = hex_to_rgb(primary)
    _, ps, pl = rgb_to_hsl(pr, pg, pb)
    primary_dark = adjust_lightness(primary, max(pl * 0.6, 10))
    primary_light = adjust_lightness(primary, min(92, 95))

    sr, sg, sb = hex_to_rgb(secondary)
    _, ss, sl = rgb_to_hsl(sr, sg, sb)
    secondary_dark = adjust_lightness(secondary, max(sl * 0.6, 10))
    secondary_light = adjust_lightness(secondary, min(92, 95))

    text_on_primary = find_safe_text_color(primary)
    text_on_secondary = find_safe_text_color(secondary)

    r, g, b = hex_to_rgb(primary)
    h, s, l = rgb_to_hsl(r, g, b)
    tinted_gray = hsl_to_rgb(h, 8, 97)
    page_bg = rgb_to_hex(*tinted_gray)

    chart_series = generate_chart_series(primary, secondary)

    pr, pg, pb = hex_to_rgb(primary)
    p_lum = luminance(pr, pg, pb)

    config = {
        "meta": {
            "company_name": company_name,
            "industry": industry,
            "style": style,
            "generated_at": datetime.now().isoformat(),
            "generator": "brand-office-suite"
        },
        "logo": {
            "color_path": "brand-assets/logo-color.png",
            "white_path": "brand-assets/logo-white.png",
            "aspect_ratio": None,
            "has_white_version": False,
            "base64_color": None,
            "base64_white": None,
            "safe_zone_ratio": 0.5,
            "primary_luminance": round(p_lum, 4)
        },
        "colors": {
            "primary": primary,
            "primary_dark": primary_dark,
            "primary_light": primary_light,
            "secondary": secondary,
            "secondary_dark": secondary_dark,
            "secondary_light": secondary_light,
            "text": {
                "primary": "#2d3748",
                "secondary": "#4a5568",
                "muted": "#8896a6",
                "on_primary": text_on_primary,
                "on_secondary": text_on_secondary
            },
            "background": {
                "page": page_bg,
                "card": "#ffffff",
                "subtle": primary_light
            },
            "border": "#e2e8f0",
            "functional": {
                "success": "#16a34a",
                "warning": "#d97706",
                "error": "#dc2626",
                "info": primary
            },
            "chart_series": chart_series
        },
        "typography": {
            "heading": fonts["heading"],
            "body": fonts["body"],
            "mono": {"family": "Consolas, 'Courier New', monospace"}
        },
        "layout": {
            "max_content_width": "1100px",
            "page_margin_cm": 2.5,
            "section_gap": "32px",
            "paragraph_gap": "16px",
            "border_radius": "6px",
            "shadow": "0 1px 3px rgba(0,0,0,0.06)"
        },
        "html": {
            "css_variables": {
                "--brand-primary": primary,
                "--brand-primary-dark": primary_dark,
                "--brand-primary-light": primary_light,
                "--brand-secondary": secondary,
                "--brand-secondary-dark": secondary_dark,
                "--brand-secondary-light": secondary_light,
                "--text-primary": "#2d3748",
                "--text-secondary": "#4a5568",
                "--text-muted": "#8896a6",
                "--bg-page": page_bg,
                "--bg-card": "#ffffff",
                "--border-color": "#e2e8f0",
                "--radius-md": "6px",
                "--shadow-card": "0 1px 3px rgba(0,0,0,0.06)"
            }
        },
        "tables": {
            "header_bg": primary,
            "header_text": text_on_primary,
            "row_alt_bg": page_bg,
            "row_bg": "#ffffff",
            "border_color": "#e2e8f0",
            "border_style": "horizontal_only"
        },
        "charts": {
            "max_pie_slices": 5,
            "line_width_px": 2,
            "data_point_radius_px": 4,
            "max_lines_per_chart": 4,
            "series_colors": chart_series
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Brand config written to {output_path}")
    return config


# ---------------------------------------------------------------------------
# embed-logo command
# ---------------------------------------------------------------------------

def embed_logo(color_path, white_path, config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if color_path and os.path.exists(color_path):
        img = Image.open(color_path)
        w, h = img.size
        config["logo"]["aspect_ratio"] = round(w / h, 4)

        with open(color_path, "rb") as img_f:
            b64 = base64.b64encode(img_f.read()).decode("utf-8")
            ext = os.path.splitext(color_path)[1].lstrip(".").lower()
            if ext == "jpg":
                ext = "jpeg"
            config["logo"]["base64_color"] = f"data:image/{ext};base64,{b64}"

    if white_path and os.path.exists(white_path):
        config["logo"]["has_white_version"] = True
        with open(white_path, "rb") as img_f:
            b64 = base64.b64encode(img_f.read()).decode("utf-8")
            ext = os.path.splitext(white_path)[1].lstrip(".").lower()
            if ext == "jpg":
                ext = "jpeg"
            config["logo"]["base64_white"] = f"data:image/{ext};base64,{b64}"

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Logo embedded into {config_path}")
    print(f"  Aspect ratio: {config['logo']['aspect_ratio']}")
    print(f"  White version: {config['logo']['has_white_version']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Brand Setup — color extraction and config generation")
    sub = parser.add_subparsers(dest="command")

    # extract-colors
    p_ext = sub.add_parser("extract-colors", help="Extract dominant colors from a logo image")
    p_ext.add_argument("--image", required=True, help="Path to logo image")
    p_ext.add_argument("--top", type=int, default=5, help="Number of colors to extract")

    # generate-config
    p_gen = sub.add_parser("generate-config", help="Generate brand-config.json from primary/secondary colors")
    p_gen.add_argument("--primary", required=True, help="Primary brand color (hex)")
    p_gen.add_argument("--secondary", required=True, help="Secondary brand color (hex)")
    p_gen.add_argument("--style", default="modern", choices=["professional", "modern", "bold", "elegant"])
    p_gen.add_argument("--industry", default="general")
    p_gen.add_argument("--company", default="", help="Company name")
    p_gen.add_argument("--output", default="brand-config.json")

    # embed-logo
    p_emb = sub.add_parser("embed-logo", help="Embed logo images as base64 into brand-config.json")
    p_emb.add_argument("--color", required=True, help="Path to color logo")
    p_emb.add_argument("--white", default=None, help="Path to white/inverse logo")
    p_emb.add_argument("--config", required=True, help="Path to brand-config.json")

    args = parser.parse_args()

    if args.command == "extract-colors":
        extract_colors(args.image, args.top)
    elif args.command == "generate-config":
        generate_config(args.primary, args.secondary, args.style, args.industry, args.company, args.output)
    elif args.command == "embed-logo":
        embed_logo(args.color, args.white, args.config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
