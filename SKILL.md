---
name: quzhi-ai-brand-office-suite
description: "Universal branded office document generation suite. Extracts brand identity from a company logo, builds a complete design system (brand-config.json), then generates professional Excel, Word, PPT, PDF, flowcharts, handbooks, and diagrams — all consistently branded. Use this skill whenever the user wants to: create branded documents for their company, set up a corporate design system, extract brand colors from a logo, generate office files (xlsx/docx/pptx/pdf) with consistent branding, produce professional reports/presentations/spreadsheets that match a corporate identity, or build a visual identity from scratch. Also triggers on: 'brand guidelines', 'company template', 'branded report', 'design system', 'corporate identity', 'brand colors', 'company style guide', or any request for professional documents that should look like they came from a specific organization."
---

# Brand Office Suite (quzhi-ai)

A two-layer system that turns any company logo into a complete branded document generation engine.

**Layer 1 — Brand Setup** (one-time): Logo → color extraction → brand interview → `brand-config.json`
**Layer 2 — Document Generation** (repeated): brand-config.json → any document type, consistently branded

## How It Works

```
User uploads logo
       ↓
Extract colors (script + visual analysis)
       ↓
3 quick questions (industry, formality, preferences)
       ↓
Generate brand-config.json (complete design tokens)
       ↓
Preview palette & sample components → user confirms
       ↓
Ready to generate any document type on demand
```

---

## Phase 1: Brand Setup

This phase runs once per company. The output — `brand-config.json` — is reused for every subsequent document.

### Step 1: Receive the Logo

When the user uploads a logo image:

1. Save it to the working directory as `brand-assets/logo-color.png`
2. Look at the image (use your vision capability) and note:
   - The dominant colors you see (be specific — "deep navy blue", not just "blue")
   - Whether the logo is geometric or organic in style
   - Whether it feels heavy/bold or light/refined
   - The approximate aspect ratio
3. Run the color extraction script for precise hex values:

```bash
python <skill-path>/scripts/brand_setup.py extract-colors --image brand-assets/logo-color.png
```

4. Ask the user if they have a **white/inverse version** of the logo (for dark backgrounds). If yes, save as `brand-assets/logo-white.png`. If no, note that only the color version is available.

### Step 2: Brand Interview (3 questions, no more)

Ask these three questions in a natural, conversational way — not as a numbered survey:

**Q1 — Industry & Audience**: "What does your company do, and who sees these documents? (e.g., 'logistics company, documents go to enterprise clients')"
- This determines font formality and visual weight

**Q2 — Style Direction**: "Which word best describes how you want your documents to feel: **professional**, **modern**, **bold**, or **elegant**?"
- Professional = conservative, serif-friendly, high contrast
- Modern = clean sans-serif, generous whitespace, flat design
- Bold = strong colors, large type, high impact
- Elegant = refined, thin fonts, subtle palette

**Q3 — Existing Rules**: "Do you have any existing brand guidelines or specific requirements? (colors you must use, fonts, do's and don'ts)"
- If they have specific hex codes, those override the extracted colors
- If they have required fonts, those override the defaults
- If they say "no" or "not really", proceed with auto-generated system

### Step 3: Generate Brand Config

Run the palette generator with the extracted colors and interview answers:

```bash
python <skill-path>/scripts/brand_setup.py generate-config \
  --primary "#extracted_hex" \
  --secondary "#extracted_hex" \
  --style "modern" \
  --industry "logistics" \
  --output brand-config.json
```

The script produces a complete `brand-config.json`. See `references/brand-config-schema.md` for the full schema.

**What the script generates from just 2 colors:**

| Token Category | What's Generated | Why It Matters |
|---|---|---|
| Color variants | Primary dark/light, secondary dark/light | Headers vs backgrounds vs subtle tints |
| Text colors | On-primary, on-secondary, primary text, muted | Contrast-safe combinations |
| Functional colors | Success, warning, error, info | Status indicators that don't clash |
| Chart palette | 5-7 harmonious colors | Data visualization consistency |
| Background set | Page, card, subtle | Visual hierarchy without brand-color overload |

### Step 4: Generate Preview

```bash
python <skill-path>/scripts/brand_preview.py --config brand-config.json --output brand-preview.html
```

This creates an HTML page showing:
- Color swatches with hex values and usage labels
- Typography samples (heading, body, mono)
- A sample table with the brand's header style
- A sample card/callout component
- A sample header and footer

Open the preview and walk the user through it: "Here's your brand system. The navy blue is your primary — used for headers and emphasis. The teal is secondary — for accents and status indicators. Does this feel right, or should we adjust anything?"

**If the user wants changes**: Modify the relevant values in `brand-config.json` directly and regenerate the preview. Common adjustments:
- "Too dark/light" → adjust primary_light or background values
- "I don't like that green" → swap the secondary color
- "Can we use a different font?" → update typography section

### Step 5: Embed Logo as Base64

Once confirmed, convert logo files to base64 for embedding in HTML/PDF:

```bash
python <skill-path>/scripts/brand_setup.py embed-logo \
  --color brand-assets/logo-color.png \
  --white brand-assets/logo-white.png \
  --config brand-config.json
```

This updates brand-config.json with `logo.base64_color` and `logo.base64_white` fields.

---

## Phase 2: Document Generation

Once brand-config.json exists, any document request follows this flow:

```
1. Load brand-config.json
2. Determine document type → read the relevant section of references/document-specs.md
3. Generate the document using brand tokens
4. Run brand compliance check
5. Deliver
```

### Routing Table

| User Says | Document Type | Method | Reference Section |
|---|---|---|---|
| "Excel", "spreadsheet", "data table" | .xlsx | openpyxl (Python) | §1 Excel |
| "Word", "document", "report", "memo" | .docx | python-docx | §2 Word |
| "PPT", "presentation", "slides", "deck" | .pptx | python-pptx | §3 PPT |
| "slides", "HTML presentation" | HTML slides | Reveal.js-style HTML | §3b HTML Slides |
| "PDF", "printable" | .pdf via HTML | HTML → Playwright | §4 PDF |
| "merge PDF", "combine PDF" | .pdf | pypdf | §4b PDF Operations |
| "flowchart", "diagram", "architecture" | HTML/SVG | Inline HTML generation | §5 Diagrams |
| "image", "poster", "banner" | .png | AI image generation | §6 Images |
| "handbook", "manual", "guide", "booklet" | .pdf via HTML | Paginated A4 HTML → PDF | §7 Handbooks |

For detailed specs on each format, read `references/document-specs.md`.

### Presentation Scene Routing

When the user requests a presentation (PPT or HTML slides), determine the narrative structure from context:

| Scene | Narrative Arc | When to Use |
|-------|--------------|-------------|
| New Client / Pitch | AIDA (Attention → Interest → Desire → Action) | Sales deck, proposal, introduction |
| Business Review | SCQA (Situation → Complication → Question → Answer) | QBR, performance review, board deck |
| Knowledge Sharing | Hero's Journey (Challenge → Discovery → Transformation) | Industry talk, training, conference |
| Internal Meeting | Pyramid (Conclusion first → Supporting data) | Status update, decision proposal |

If the user doesn't specify, ask: "This presentation is for what scenario — pitching a client, reviewing business, sharing knowledge, or an internal meeting?"

### Universal Rules (All Formats)

These rules apply to every document generated, regardless of format:

**Color Usage Discipline**
- Primary color: headers, titles, emphasis, table header backgrounds
- Primary light: subtle backgrounds, hover states, alternate table rows (at 10-15% opacity feel)
- Secondary color: accents, tags, status indicators, chart highlights — never large areas
- Neutral text colors: body text (never use brand colors for body text)
- Functional colors: only for status/alerts, never decorative

The most common amateur mistake: using the primary color for everything. A branded document uses the primary color in **3-5 strategic places**, not on every element.

**60-30-10 Color Ratio** (especially for presentations):
- 60% — Neutral (white/light background, body text)
- 30% — Primary brand color (headers, key sections, cover backgrounds)
- 10% — Secondary/accent (highlights, CTAs, data emphasis)

**Logo Placement**
- Only set ONE dimension (width OR height), let the other be auto
- Respect the aspect ratio from brand-config.json (never stretch or squish)
- Auto-detect background brightness: `luminance = R×0.2126 + G×0.7152 + B×0.0722` (0-255 scale). If luminance < 128 → white logo; else → color logo
- Maintain safe zone: 50% of logo height as minimum clearance on all sides

**Typography**
- Headings: heading font at specified weight
- Body: body font at regular weight
- Code/data: mono font
- Never mix more than these 3 font families in one document

**Anti-AI Aesthetic (Critical)**
These patterns scream "AI generated" and destroy credibility:
- ✗ Gradient backgrounds (especially blue-purple)
- ✗ Emoji as decorative elements in professional documents
- ✗ Rounded-corner cards with left color bars (the ChatGPT look)
- ✗ Icons before every single bullet point
- ✗ 3D pie charts or fake 3D effects
- ✗ More than 3 primary colors fighting for attention
- ✗ Buzzwords: "赋能", "助力", "在当今快速变化的..."
- ✗ Stock photo collages filling entire pages

Instead:
- ✓ Large intentional whitespace (40% empty is good design, not waste)
- ✓ High contrast (dark titles + light body)
- ✓ Precise grid alignment
- ✓ Data labels directly on charts (not separate legends when possible)
- ✓ One core message per slide/section
- ✓ Thin line separators instead of color blocks
- ✓ Pure solid colors, never gradients (except: one subtle gradient on a cover page is acceptable)

---

## Quality Gate

Before delivering any generated document, run the brand compliance checker:

```bash
python <skill-path>/scripts/brand_check.py --config brand-config.json --file <output-file>
```

The checker verifies:
- All colors used are from the brand config (no rogue hex values)
- Logo aspect ratio is preserved
- Text-on-background combinations meet WCAG AA contrast (4.5:1 for body text)
- No prohibited patterns (gradients in non-cover contexts, emoji decorations)
- Font families match the config

**Only deliver files that pass all checks.** If a check fails, fix the issue and re-run.

---

## File Organization

```
{working-directory}/
├── brand-assets/
│   ├── logo-color.png          ← User's color logo
│   └── logo-white.png          ← White version (if provided)
├── brand-config.json           ← The design system (source of truth)
├── brand-preview.html          ← Visual preview of the brand system
└── outputs/
    └── {generated files}       ← All generated documents go here
```

---

## Edge Cases

**User has no logo**: Skip color extraction. Ask them to pick a primary and secondary color (offer a few industry-appropriate suggestions). Generate brand-config.json from those choices. Note in the config that no logo is available — documents will use company name text instead of a logo image.

**User has full brand guidelines already**: Skip the interview. Ask them to share their guidelines (PDF, website, or just tell you the rules). Manually populate brand-config.json with their specified values. The script's auto-generation is a fallback for users without existing guidelines, not a replacement for deliberate brand work.

**User wants to update their brand**: Re-run Phase 1. The old brand-config.json is overwritten. Previously generated documents are not retroactively updated (tell the user this).

**Multiple brands / sub-brands**: Create separate brand-config files (e.g., `brand-config-subsidiary.json`). When generating a document, specify which config to use.

---

## Dependencies (Auto-Install)

This skill is self-contained. All required Python packages are listed in `requirements.txt` and will be installed automatically on first use.

### First-Time Setup (runs once, automatically)

Before executing any script in this skill, check whether dependencies are installed:

```bash
python -c "import PIL, openpyxl, docx, pptx, pypdf, pdfplumber" 2>/dev/null || pip install -r <skill-path>/requirements.txt
```

If the import check fails, `pip install` runs automatically. The user only needs to click "Allow" once on the permission prompt. After that, all document types (Excel, Word, PPT, PDF, flowcharts) are available immediately.

### Optional: HTML→PDF Conversion

For converting HTML documents to PDF, Playwright with Chromium is needed. This is **optional** — if not installed, the skill outputs HTML which the user can print to PDF from their browser.

```bash
pip install playwright && playwright install chromium
```

If Playwright is not available when PDF is requested, inform the user: "I've generated the HTML version. You can open it in your browser and print to PDF (Ctrl+P → Save as PDF). Or I can install Playwright for automatic PDF conversion — want me to do that?"
