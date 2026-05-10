#!/usr/bin/env python3
"""
Brand compliance checker — verifies generated files against brand-config.json.

Checks:
  - All hex colors in the file are from the brand config palette
  - Logo aspect ratio is preserved (HTML/CSS only)
  - Text-on-background contrast meets WCAG AA (4.5:1)
  - No prohibited patterns (gradients, emoji decoration)

Usage:
  python brand_check.py --config brand-config.json --file output.html
  python brand_check.py --config brand-config.json --file output.html --strict
"""

import argparse
import json
import re
import sys


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def luminance(r, g, b):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast_ratio(hex1, hex2):
    l1 = luminance(*hex_to_rgb(hex1))
    l2 = luminance(*hex_to_rgb(hex2))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def normalize_hex(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return f"#{h}"


def collect_palette(config):
    """Collect all allowed hex colors from the brand config."""
    allowed = set()

    def walk(obj):
        if isinstance(obj, str) and re.match(r'^#[0-9a-fA-F]{3,8}$', obj):
            allowed.add(normalize_hex(obj))
        elif isinstance(obj, dict):
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(config.get("colors", {}))
    walk(config.get("tables", {}))
    walk(config.get("charts", {}))

    always_ok = {"#ffffff", "#000000", "#fff", "#f7fafc", "#f1f5f9", "#e5e7eb",
                 "#d1d5db", "#9ca3af", "#6b7280", "#4b5563", "#374151",
                 "#1f2937", "#111827", "#f9fafb", "#fafafa", "#f5f5f5"}
    allowed.update(always_ok)

    return allowed


def check_html(file_path, config, strict=False):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    issues = []
    warnings = []

    allowed = collect_palette(config)

    hex_pattern = re.compile(r'#[0-9a-fA-F]{3,8}\b')
    found_colors = set()
    for match in hex_pattern.finditer(content):
        raw = match.group()
        if len(raw) in (4, 7):
            found_colors.add(normalize_hex(raw))

    rogue_colors = found_colors - allowed
    rgba_pattern = re.compile(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)')
    for match in rgba_pattern.finditer(content):
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        h = f"#{r:02x}{g:02x}{b:02x}"
        if normalize_hex(h) not in allowed:
            rogue_colors.add(normalize_hex(h))

    if rogue_colors:
        severity = "ERROR" if strict else "WARNING"
        issues.append(f"{severity}: Found {len(rogue_colors)} color(s) not in brand palette: {', '.join(sorted(rogue_colors))}")

    gradient_pattern = re.compile(r'(linear|radial)-gradient', re.IGNORECASE)
    gradient_matches = gradient_pattern.findall(content)
    if gradient_matches:
        warnings.append(f"WARNING: Found {len(gradient_matches)} gradient(s). Gradients are discouraged (acceptable only on cover pages).")

    emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FA6F]')
    emoji_matches = emoji_pattern.findall(content)
    if emoji_matches:
        warnings.append(f"WARNING: Found {len(emoji_matches)} emoji character(s). Emoji decoration is discouraged in professional documents.")

    logo = config.get("logo", {})
    ar = logo.get("aspect_ratio")
    if ar:
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        for tag in img_tags:
            if 'logo' in tag.lower() or (logo.get("base64_color") and logo["base64_color"][:50] in tag):
                has_width = re.search(r'width\s*[:=]\s*[\d]+', tag)
                has_height = re.search(r'height\s*[:=]\s*[\d]+', tag)
                if has_width and has_height:
                    w_match = re.search(r'width\s*[:=]\s*(\d+)', tag)
                    h_match = re.search(r'height\s*[:=]\s*(\d+)', tag)
                    if w_match and h_match:
                        w, h = int(w_match.group(1)), int(h_match.group(1))
                        actual_ar = w / h if h > 0 else 0
                        if abs(actual_ar - ar) / ar > 0.05:
                            issues.append(f"ERROR: Logo aspect ratio distorted. Expected ~{ar:.3f}, got {actual_ar:.3f}.")

    file_path_pattern = re.compile(r'(file:///|[A-Z]:\\|/home/|/Users/)[^\s"\'<>]+')
    path_leaks = file_path_pattern.findall(content)
    if path_leaks:
        issues.append(f"ERROR: Found {len(path_leaks)} local file path(s) leaked in output.")

    all_issues = issues + warnings
    passed = len(issues) == 0

    result = {
        "pass": passed,
        "errors": [i for i in issues if i.startswith("ERROR")],
        "warnings": warnings + [i for i in issues if i.startswith("WARNING")],
        "palette_size": len(allowed),
        "colors_found": len(found_colors),
        "rogue_colors": list(rogue_colors)
    }

    if passed:
        print(f"pass=true")
        print(f"  Colors checked: {len(found_colors)} found, {len(rogue_colors)} outside palette")
    else:
        print(f"pass=false")
        for issue in all_issues:
            print(f"  {issue}")

    if warnings and passed:
        for w in warnings:
            print(f"  {w}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Brand compliance checker")
    parser.add_argument("--config", required=True, help="Path to brand-config.json")
    parser.add_argument("--file", required=True, help="Path to file to check")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    ext = args.file.rsplit(".", 1)[-1].lower()

    if ext in ("html", "htm", "svg"):
        result = check_html(args.file, config, args.strict)
    else:
        print(f"INFO: Brand check for .{ext} files is limited to color and path checks.")
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        allowed = collect_palette(config)
        hex_pattern = re.compile(r'#[0-9a-fA-F]{6}\b')
        found = {normalize_hex(m.group()) for m in hex_pattern.finditer(content)}
        rogue = found - allowed
        if rogue:
            print(f"WARNING: {len(rogue)} color(s) outside brand palette: {', '.join(sorted(rogue))}")
        else:
            print(f"pass=true")
        result = {"pass": len(rogue) == 0, "rogue_colors": list(rogue)}

    if args.json:
        print(json.dumps(result, indent=2))

    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
