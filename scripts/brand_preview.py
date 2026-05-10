#!/usr/bin/env python3
"""
Generate an HTML preview page for a brand-config.json design system.
Shows color swatches, typography, sample table, sample card, and header/footer.

Usage:
  python brand_preview.py --config brand-config.json --output brand-preview.html
"""

import argparse
import json
import sys


def generate_preview(config_path, output_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    c = config["colors"]
    t = config["typography"]
    meta = config.get("meta", {})
    logo = config.get("logo", {})
    tables = config.get("tables", {})

    company = meta.get("company_name", "Your Company")
    style = meta.get("style", "modern")

    heading_font = t["heading"]["family_web"]
    body_font = t["body"]["family_web"]

    logo_img = ""
    if logo.get("base64_color"):
        ar = logo.get("aspect_ratio", 2.0)
        logo_img = f'<img src="{logo["base64_color"]}" style="height:40px;width:auto;" alt="Logo">'

    logo_white_img = ""
    if logo.get("base64_white"):
        logo_white_img = f'<img src="{logo["base64_white"]}" style="height:40px;width:auto;" alt="Logo White">'
    elif logo_img:
        logo_white_img = logo_img

    chart_swatches = ""
    for i, color in enumerate(c.get("chart_series", [])):
        chart_swatches += f'<div style="width:48px;height:48px;background:{color};border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;">{i+1}</div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brand Preview — {company}</title>
<style>
  :root {{
    --brand-primary: {c["primary"]};
    --brand-primary-dark: {c["primary_dark"]};
    --brand-primary-light: {c["primary_light"]};
    --brand-secondary: {c["secondary"]};
    --text-primary: {c["text"]["primary"]};
    --text-secondary: {c["text"]["secondary"]};
    --text-muted: {c["text"]["muted"]};
    --bg-page: {c["background"]["page"]};
    --bg-card: {c["background"]["card"]};
    --border-color: {c["border"]};
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: {body_font};
    color: var(--text-primary);
    background: var(--bg-page);
    line-height: 1.6;
  }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 40px 24px; }}
  h1 {{ font-family: {heading_font}; font-weight: {t["heading"]["weight"]}; font-size: 28px; margin-bottom: 8px; }}
  h2 {{ font-family: {heading_font}; font-weight: {t["heading"]["weight"]}; font-size: 20px; margin: 40px 0 16px; color: var(--brand-primary); }}
  h3 {{ font-family: {heading_font}; font-size: 16px; margin: 24px 0 12px; }}
  .subtitle {{ color: var(--text-muted); font-size: 14px; margin-bottom: 32px; }}

  /* Header sample */
  .sample-header {{
    background: var(--brand-primary);
    color: {c["text"]["on_primary"]};
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 6px 6px 0 0;
    margin-bottom: 0;
  }}
  .sample-header h3 {{ color: {c["text"]["on_primary"]}; margin: 0; font-size: 18px; }}

  /* Swatch grid */
  .swatch-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }}
  .swatch {{
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    background: var(--bg-card);
  }}
  .swatch-color {{ height: 64px; }}
  .swatch-info {{ padding: 8px 10px; font-size: 12px; }}
  .swatch-hex {{ font-family: {t["mono"]["family"]}; color: var(--text-secondary); }}
  .swatch-label {{ font-weight: 600; display: block; margin-bottom: 2px; }}

  /* Table sample */
  .sample-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  .sample-table th {{
    background: {tables.get("header_bg", c["primary"])};
    color: {tables.get("header_text", c["text"]["on_primary"])};
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
  }}
  .sample-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-color);
    font-size: 13px;
  }}
  .sample-table tr:nth-child(even) td {{ background: {tables.get("row_alt_bg", c["background"]["page"])}; }}

  /* Card sample */
  .sample-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin: 16px 0;
  }}
  .sample-card .card-title {{
    font-family: {heading_font};
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 8px;
    color: var(--brand-primary);
  }}

  /* Callout */
  .sample-callout {{
    border-left: 3px solid var(--brand-primary);
    background: var(--brand-primary-light);
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 16px 0;
    font-size: 14px;
  }}

  /* Footer sample */
  .sample-footer {{
    background: var(--bg-page);
    border-top: 1px solid var(--border-color);
    padding: 16px 32px;
    font-size: 12px;
    color: var(--text-muted);
    text-align: center;
    border-radius: 0 0 6px 6px;
  }}

  /* Chart series */
  .chart-series {{ display: flex; gap: 8px; flex-wrap: wrap; }}

  /* Typography sample */
  .type-sample {{ margin: 8px 0; }}
  .type-label {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }}

  .section {{ margin-bottom: 48px; }}
</style>
</head>
<body>
<div class="container">

  <h1>Brand System Preview</h1>
  <p class="subtitle">{company} &middot; {style} style &middot; Generated by Brand Office Suite</p>

  <!-- COLORS -->
  <div class="section">
    <h2>Color Palette</h2>

    <h3>Brand Colors</h3>
    <div class="swatch-grid">
      <div class="swatch">
        <div class="swatch-color" style="background:{c['primary']};"></div>
        <div class="swatch-info"><span class="swatch-label">Primary</span><span class="swatch-hex">{c['primary']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['primary_dark']};"></div>
        <div class="swatch-info"><span class="swatch-label">Primary Dark</span><span class="swatch-hex">{c['primary_dark']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['primary_light']};"></div>
        <div class="swatch-info"><span class="swatch-label">Primary Light</span><span class="swatch-hex">{c['primary_light']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['secondary']};"></div>
        <div class="swatch-info"><span class="swatch-label">Secondary</span><span class="swatch-hex">{c['secondary']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['secondary_dark']};"></div>
        <div class="swatch-info"><span class="swatch-label">Secondary Dark</span><span class="swatch-hex">{c['secondary_dark']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['secondary_light']};"></div>
        <div class="swatch-info"><span class="swatch-label">Secondary Light</span><span class="swatch-hex">{c['secondary_light']}</span></div>
      </div>
    </div>

    <h3>Text Colors</h3>
    <div class="swatch-grid">
      <div class="swatch">
        <div class="swatch-color" style="background:{c['text']['primary']};"></div>
        <div class="swatch-info"><span class="swatch-label">Text Primary</span><span class="swatch-hex">{c['text']['primary']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['text']['secondary']};"></div>
        <div class="swatch-info"><span class="swatch-label">Text Secondary</span><span class="swatch-hex">{c['text']['secondary']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['text']['muted']};"></div>
        <div class="swatch-info"><span class="swatch-label">Text Muted</span><span class="swatch-hex">{c['text']['muted']}</span></div>
      </div>
    </div>

    <h3>Functional Colors</h3>
    <div class="swatch-grid">
      <div class="swatch">
        <div class="swatch-color" style="background:{c['functional']['success']};"></div>
        <div class="swatch-info"><span class="swatch-label">Success</span><span class="swatch-hex">{c['functional']['success']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['functional']['warning']};"></div>
        <div class="swatch-info"><span class="swatch-label">Warning</span><span class="swatch-hex">{c['functional']['warning']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['functional']['error']};"></div>
        <div class="swatch-info"><span class="swatch-label">Error</span><span class="swatch-hex">{c['functional']['error']}</span></div>
      </div>
      <div class="swatch">
        <div class="swatch-color" style="background:{c['functional']['info']};"></div>
        <div class="swatch-info"><span class="swatch-label">Info</span><span class="swatch-hex">{c['functional']['info']}</span></div>
      </div>
    </div>

    <h3>Chart Series</h3>
    <div class="chart-series">
      {chart_swatches}
    </div>
  </div>

  <!-- TYPOGRAPHY -->
  <div class="section">
    <h2>Typography</h2>
    <div class="type-sample">
      <div class="type-label">Heading — {heading_font.split(',')[0].strip("'")}, {t['heading']['weight']}</div>
      <div style="font-family:{heading_font};font-weight:{t['heading']['weight']};font-size:28px;">The quick brown fox jumps over the lazy dog</div>
    </div>
    <div class="type-sample">
      <div class="type-label">Body — {body_font.split(',')[0].strip("'")}, {t['body']['weight']}</div>
      <div style="font-family:{body_font};font-weight:{t['body']['weight']};font-size:15px;line-height:1.7;">
        Professional documents require consistent typography to establish visual hierarchy and maintain readability across different contexts.
        The body font should be comfortable to read at length, while headings create clear section breaks.
      </div>
    </div>
    <div class="type-sample">
      <div class="type-label">Monospace — {t['mono']['family'].split(',')[0]}</div>
      <div style="font-family:{t['mono']['family']};font-size:13px;background:#f1f5f9;padding:12px;border-radius:4px;">
        const config = loadBrandConfig("brand-config.json");<br>
        console.log(config.colors.primary); // {c['primary']}
      </div>
    </div>
  </div>

  <!-- COMPONENTS -->
  <div class="section">
    <h2>Components</h2>

    <h3>Header</h3>
    <div class="sample-header">
      {logo_white_img if logo_white_img else f'<span style="font-weight:700;font-size:16px;">{company}</span>'}
      <h3>Quarterly Business Review</h3>
    </div>

    <h3>Data Table</h3>
    <table class="sample-table">
      <thead>
        <tr><th>Department</th><th>Q1 Revenue</th><th>Q1 Target</th><th>Achievement</th></tr>
      </thead>
      <tbody>
        <tr><td>Sales</td><td>¥2,450,000</td><td>¥2,300,000</td><td style="color:{c['functional']['success']};">107%</td></tr>
        <tr><td>Operations</td><td>¥1,820,000</td><td>¥1,900,000</td><td style="color:{c['functional']['error']};">96%</td></tr>
        <tr><td>Product</td><td>¥980,000</td><td>¥950,000</td><td style="color:{c['functional']['success']};">103%</td></tr>
        <tr><td>Finance</td><td>¥650,000</td><td>¥640,000</td><td style="color:{c['functional']['success']};">102%</td></tr>
      </tbody>
    </table>

    <h3>Card</h3>
    <div class="sample-card">
      <div class="card-title">Key Insight</div>
      <p style="font-size:14px;">Sales department exceeded Q1 targets by 7%, driven primarily by new client acquisition in the logistics sector. Operations fell short by 4% due to seasonal capacity constraints.</p>
    </div>

    <h3>Callout</h3>
    <div class="sample-callout">
      This is an informational callout block — used for important notes, tips, or contextual information that should stand out from the main content.
    </div>

    <h3>Footer</h3>
    <div class="sample-footer">
      {company} &middot; Confidential &middot; Generated by Brand Office Suite
    </div>
  </div>

</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate brand system preview HTML")
    parser.add_argument("--config", required=True, help="Path to brand-config.json")
    parser.add_argument("--output", default="brand-preview.html", help="Output HTML path")
    args = parser.parse_args()
    generate_preview(args.config, args.output)


if __name__ == "__main__":
    main()
