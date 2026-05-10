**🌐 English** · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

<h1 align="center">logo2docs</h1>

<p align="center">
  <em>"One logo in. A complete branded document suite out."</em><br>
  <em>「一个 LOGO，全套品牌文档。」</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://skills.sh"><img src="https://img.shields.io/badge/skills.sh-Compatible-brightgreen" alt="skills.sh"></a>
  <a href="#"><img src="https://img.shields.io/badge/Agent-Agnostic-blueviolet" alt="Agent Agnostic"></a>
</p>

**Upload a company logo — get consistently branded Excel, Word, PowerPoint, HTML slides, PDF, flowcharts & handbooks.** All design-system-driven. All editable. No Figma, no templates, no design skills needed.

PowerPoint files are real `.pptx` — open in PowerPoint / WPS / Keynote, change anything. Want cinematic animations? Choose HTML mode.

```
npx skills add quzhi-ai/logo2docs
```

[See demos](#demos) · [Install](#install) · [How it works](#how-it-works) · [Design principles](#design-principles) · [Color science](#how-the-color-science-works)

---

## How It Works

A two-layer system:

1. **Brand Setup** (one-time) — Extract colors from a logo → 3 quick questions → complete design system `brand-config.json` with 40+ design tokens
2. **Document Generation** (on-demand) — Generate any document type, all consistently branded

```
Upload logo → Extract colors → 3 questions → brand-config.json → Any document type
```

### Supported Document Types

| Format | Method | Output |
|--------|--------|--------|
| Excel spreadsheet | openpyxl | `.xlsx` |
| Word document | python-docx | `.docx` |
| PowerPoint deck | python-pptx | `.pptx` |
| HTML presentation | Inline HTML/CSS/JS | `.html` |
| PDF (via HTML) | HTML → browser print | `.html` / `.pdf` |
| Flowchart / diagram | Inline SVG | `.html` |
| Handbook / manual | Paginated A4 HTML | `.html` / `.pdf` |

### What `brand-config.json` generates from just 2 colors

| Category | Tokens | Purpose |
|----------|--------|---------|
| Color variants | Primary dark/light, secondary dark/light | Headers vs. backgrounds vs. tints |
| Text colors | On-primary, on-secondary, body, muted | Contrast-safe text combinations |
| Functional colors | Success, warning, error, info | Status indicators that don't clash |
| Chart palette | 5-7 harmonious colors | Data visualization consistency |
| Background set | Page, card, subtle | Visual hierarchy layers |
| Typography | Heading, body, mono (web + office) | Cross-format font consistency |
| Layout tokens | Margins, gaps, radii, shadows | Spatial consistency |
| CSS variables | Full `:root` block | Drop-in HTML theming |

---

## Install

```bash
npx skills add quzhi-ai/logo2docs
```

Or manually: clone this repo and copy the contents into your Claude Code skills directory.

Then just tell Claude:

> "Here's our company logo. Set up our brand system and generate a quarterly report in Excel."

Claude will:
1. Analyze your logo colors
2. Ask 3 quick questions (industry, style preference, existing guidelines)
3. Generate `brand-config.json` — your complete design system
4. Produce the requested document with consistent branding

---

## Design Principles

### Anti-AI Aesthetic

Documents look like a professional designer made them, not an AI:

- No gradient backgrounds (especially blue-purple)
- No emoji as decoration in professional documents
- No rounded-corner cards with colored left borders
- No 3D pie charts or fake 3D effects
- Large intentional whitespace (40% empty is good design)
- High contrast, precise grid alignment
- Solid colors only, thin line separators

### 60-30-10 Color Rule

- **60%** — Neutral (white/light backgrounds, body text)
- **30%** — Primary brand color (headers, key sections)
- **10%** — Secondary/accent (highlights, data emphasis)

### WCAG Contrast

All text-on-background combinations are checked against WCAG AA standards (4.5:1 minimum contrast ratio).

---

## Demos

### ABC Education (Bold style)
Children's education company — coral red + teal. Excel, Word, PowerPoint, HTML slides, flowchart.

<p align="center">
<img src="demos/screenshots/abc-01-cover.png" width="400"> <img src="demos/screenshots/abc-02-content.png" width="400"><br>
<img src="demos/screenshots/abc-05-excel.png" width="400"> <img src="demos/screenshots/abc-06-word.png" width="400"><br>
<img src="demos/screenshots/abc-03-data.png" width="400"> <img src="demos/screenshots/abc-04-preview.png" width="400">
</p>

### PuYe Wellness (Elegant style)
Premium wellness tea brand — olive green + warm apricot. PowerPoint, HTML handbook (8-page A4).

<p align="center">
<img src="demos/screenshots/puye-01-cover.png" width="400"> <img src="demos/screenshots/puye-02-story.png" width="400"><br>
<img src="demos/screenshots/puye-03-plans.png" width="400"> <img src="demos/screenshots/puye-04-data.png" width="400">
</p>

---

## How the Color Science Works

1. **Extract**: Resize logo to 150x150, quantize colors (16-step), cluster similar colors (distance < 40), rank by frequency
2. **Expand**: From 2 base colors, generate dark/light variants via HSL lightness adjustment, find WCAG-safe text colors, create harmonious chart series via hue rotation
3. **Validate**: Every text/background pair is checked for WCAG AA contrast (4.5:1 minimum)

---

## File Structure

```
logo2docs/
├── SKILL.md              # Skill definition (read by Claude)
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── brand_setup.py    # Color extraction + config generation
│   ├── brand_preview.py  # HTML preview of design system
│   └── brand_check.py    # Brand compliance checker
├── references/
│   ├── brand-config-schema.md   # Full config schema docs
│   └── document-specs.md        # Per-format generation specs
├── evals/
│   └── evals.json        # Evaluation prompts
└── demos/
    ├── abc-education/     # Bold style demo
    └── puye-wellness/     # Elegant style demo
```

## Dependencies

All Python packages are auto-installed on first use:

```
Pillow          # Logo color extraction
openpyxl        # Excel generation
python-docx     # Word generation
python-pptx     # PowerPoint generation
pypdf           # PDF operations
pdfplumber      # PDF reading
```

Optional: [Playwright](https://playwright.dev/) for automatic HTML-to-PDF conversion. Without it, HTML documents can be printed to PDF from any browser.

---

## Support the Project

If logo2docs has been helpful, consider buying the author a coffee:

| WeChat Pay | Alipay |
|:---:|:---:|
| <img src="demos/donate/wechat-pay.jpg" width="200"> | <img src="demos/donate/alipay.jpg" width="200"> |

## Star History

<p align="center">
  <a href="https://star-history.com/#quzhi-ai/logo2docs&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date" width="600" />
    </picture>
  </a>
</p>

## License

MIT — see [LICENSE](LICENSE)

---

<p align="center">
  <a href="https://x.com/quzhiai"><img src="https://img.shields.io/badge/X%20%2F%20Twitter-@quzhiai-black?logo=x&logoColor=white" alt="X / Twitter"></a>
</p>
