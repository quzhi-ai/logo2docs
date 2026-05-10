# Document Generation Specifications

This reference covers format-specific rules for each document type. Load the relevant section when generating a document — don't load the whole file every time.

## Table of Contents

1. [Excel (.xlsx)](#1-excel-xlsx)
2. [Word (.docx)](#2-word-docx)
3. [PPT (.pptx)](#3-ppt-pptx)
4. [HTML Slides](#3b-html-slides)
5. [PDF (via HTML)](#4-pdf-via-html)
6. [PDF Operations](#4b-pdf-operations)
7. [Flowcharts & Diagrams](#5-flowcharts--diagrams)
8. [Branded Images](#6-branded-images)
9. [Handbooks & Long Documents](#7-handbooks--long-documents)

---

## §1 Excel (.xlsx)

**Library**: `openpyxl`

### Structure

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import json

with open("brand-config.json") as f:
    brand = json.load(f)

# Extract brand values
primary = brand["colors"]["primary"].lstrip("#")
on_primary = brand["colors"]["text"]["on_primary"].lstrip("#")
alt_bg = brand["tables"]["row_alt_bg"].lstrip("#")
border_color = brand["colors"]["border"].lstrip("#")
heading_font = brand["typography"]["heading"]["family_office"]
body_font = brand["typography"]["body"]["family_office"]
```

### Styling Rules

| Element | Style |
|---------|-------|
| Header row | Fill: primary color, Font: white (on_primary), Bold, 11pt heading font |
| Body cells | Font: body font, 10pt, text.primary color |
| Alternating rows | Even rows get alt_bg fill |
| Borders | Bottom border only (border_color), no vertical lines |
| Column width | Auto-fit content + 2 char padding, min 10 chars |
| Number format | Use locale-appropriate format (#,##0 for integers, #,##0.00 for decimals) |
| Percentage | 0.0% format, conditional color (success if >= target, error if below) |
| Title row | Row 1: company name in primary color, bold, 14pt, merged across columns |

### Financial Color Coding Standard

When generating financial/analytical spreadsheets, apply this industry-standard color convention:

| Cell Type | Font Color | Meaning |
|-----------|-----------|---------|
| Manual inputs | Blue | Values the user types in |
| Formulas | Black | Calculated cells |
| Cross-sheet references | Green | Links to other sheets in the workbook |
| External references | Red | Links to other files |
| Assumption cells | Yellow background | Key assumptions that drive the model |

### Formula-First Principle

All calculations must be done with Excel formulas (`=SUM()`, `=AVERAGE()`, `=IF()`, etc.), not hardcoded Python values. The spreadsheet must remain dynamic — when a user changes an input cell, all dependent cells should recalculate automatically.

```python
# ✓ Correct: formula in Excel
ws["C2"] = "=A2*B2"

# ✗ Wrong: pre-calculated in Python
ws["C2"] = price * quantity
```

### Meaningful Sheet Names

Every sheet must have a descriptive name (not "Sheet1", "Sheet2"). Examples: "Revenue Summary", "Q3 Actuals", "Assumptions". Enforced at validation.

### Chart Styling (openpyxl charts)

- Use `chart_series` colors from brand config
- No 3D effects, no default Excel color palette
- Data labels directly on chart when ≤ 5 data points
- Max 5 pie slices (group others into "Other")
- Grid lines: light gray (#e5e7eb), not black
- Remove chart border/outline
- Bar chart gap-to-width ratio: 0.6×
- Right-align numeric axis labels

---

## §2 Word (.docx)

**Library**: `python-docx`

### Page Setup

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
section = doc.sections[0]
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)
```

### Heading Hierarchy

| Level | Size | Color | Weight |
|-------|------|-------|--------|
| Title | 18pt | primary | Bold |
| Heading 1 | 16pt | primary | Bold |
| Heading 2 | 13pt | primary_dark | Bold |
| Heading 3 | 11pt | text.primary | Bold |
| Body | 10.5pt | text.primary | Regular |
| Caption | 9pt | text.muted | Regular |

### Table Style

- Header row: primary background, white text, bold
- Body: alternating white / page_bg
- Borders: horizontal lines only in border_color
- Cell padding: 0.1cm vertical, 0.2cm horizontal
- Text alignment: text left, numbers right

### Header/Footer

- Header: Logo (if available) right-aligned, document title left-aligned
- Footer: Page number center, company name left, "Confidential" right
- Font: 8pt, text.muted color

### Logo Insertion

```python
from docx.shared import Cm

# Calculate width from aspect ratio
logo_height_cm = 1.2
logo_width_cm = logo_height_cm * brand["logo"]["aspect_ratio"]
doc.sections[0].header.paragraphs[0].add_run().add_picture(
    "brand-assets/logo-color.png",
    height=Cm(logo_height_cm)
)
```

---

## §3 PPT (.pptx)

**Library**: `python-pptx`

### Slide Dimensions

Standard 16:9 widescreen: 13.333" × 7.5" (33.867cm × 19.05cm)

### Safe Area Definition

Based on 1920×1080 baseline:
- Left/right margins: 80px (1.4")
- Top margin: 120px (1.2")
- Bottom margin: 100px
- Inter-element spacing: ≥ 30px

### Layout Zones

```
┌──────────────────────────────────────────┐
│ LOGO (top-right)    TITLE (top-left)     │ ← Header: 0-1.2"
├──────────────────────────────────────────┤
│                                          │
│              CONTENT AREA                │ ← Main: 1.2-6.3"
│         (margins: 1.4" L/R)             │
│                                          │
├──────────────────────────────────────────┤
│           BRAND STRIPE / FOOTER          │ ← Footer: 6.3-7.5"
└──────────────────────────────────────────┘
```

### Slide Types

**Cover Slide**
- Full-width primary color background
- Company name + presentation title centered
- Logo top-right (white version on dark bg)
- One subtle gradient acceptable here (and only here)

**Section Divider**
- Primary color background, large white title text centered
- Optional secondary color accent stripe at bottom

**Content Slide**
- White/page_bg background
- Title in primary color at top-left
- Content area with generous margins
- Logo small in corner (color version on light bg)

**Data Slide**
- Same as content but optimized for tables/charts
- Use full content width for data elements

### Font Sizes (PPT)

| Element | Size |
|---------|------|
| Cover title | 44pt Bold |
| Section title | 32pt Bold |
| Slide title | 26pt Bold |
| Body text | 20pt Regular |
| Caption/footnote | 14pt Regular |
| Data in tables | 16pt Regular |

### Font Pairing Strategy

- Heading font: personality font (conveys brand tone)
- Body font: legibility font (optimized for reading)
- Never use the same font for both unless the brand specifically requires it
- Recommended safe pairings:
  - Professional: Calibri headings + Calibri Light body
  - Modern: Arial headings + Segoe UI body
  - Elegant: Georgia headings + Garamond body

### Shape Styling

- Rectangles: 4-6px corner radius, no shadow (unless card effect needed)
- Lines: 1.5-2px, primary or border color
- Arrows: solid, not 3D
- No clip art, no stock icons, no WordArt

### Quality Checks (PPT-Specific)

- Text does not overflow any shape boundaries
- No text-on-shape overlap (text visible through shapes)
- All slides have ≥ 0.5" from content to edges
- No placeholder content ("XXXX", "Lorem ipsum", "[Insert here]")
- Dark text on light backgrounds, light text on dark backgrounds

---

## §3b HTML Slides

For HTML-based presentations (Reveal.js style). Use when the user prefers browser-based slides over .pptx.

### Font Sizes

Use `pt` units for slides (predictable, like PowerPoint), NOT px/em/rem:

| Element | Size |
|---------|------|
| Cover title | `clamp(28pt, 4vw, 44pt)` |
| Section title | `clamp(24pt, 3vw, 36pt)` |
| Slide title | `clamp(20pt, 2.5vw, 28pt)` |
| Body text | `clamp(14pt, 1.8vw, 20pt)` |

### Layout Rules

- Each slide's grid/flex layout is inlined (column ratios and gaps vary per slide)
- Do NOT use generic utility classes like `.grid-2` — each slide has unique content needs
- Wrap text content in `<div class="content">` for consistent flexbox vertical flow
- Use `<section>` for horizontal slides, nested `<section>` for vertical drill-downs

### Navigation

Include keyboard (← → ↑ ↓), scroll, and touch navigation. Auto-sync progress bar and page indicators.

### Progressive Reveal

For complex topics, use vertical slide stacks: main point on horizontal slide, supporting detail on vertical sub-slides below.

### Export

For users who need a .pptx or PDF version of HTML slides:
- HTML → PDF: Use Playwright with exact viewport (1920×1080)
- HTML → Images: Capture each slide as PNG at 150 dpi for insertion into other tools

---

## §4 PDF (via HTML)

PDFs are generated by creating an HTML document and converting it with a headless browser.

### HTML Template Structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=...');

    @page {
      size: A4;
      margin: 2cm;
    }
    :root {
      /* Paste all CSS variables from brand-config.json html.css_variables */
    }
    body {
      font-family: /* body.family_web */;
      color: var(--text-primary);
      background: #ffffff;
      line-height: 1.6;
      max-width: /* layout.max_content_width */;
      margin: 0 auto;
    }
    @media print {
      body { background: white; }
      .no-print { display: none; }
      a { text-decoration: none; color: inherit; }
      box-shadow: none;
    }
  </style>
</head>
<body>
  <header> <!-- brand header with logo --> </header>
  <main> <!-- content --> </main>
  <footer> <!-- brand footer --> </footer>
</body>
</html>
```

### HTML-Specific Rules

- **Header**: Solid primary background (no gradient), white logo, document title
- **Logo embedding**: Always use base64 data URI from brand-config.json (never local file paths)
- **Page breaks**: Use `page-break-before: always` for section dividers
- **Print styles**: Include `@media print` block that removes shadows, simplifies borders
- **Max width**: Content constrained to layout.max_content_width, centered
- **Tables**: Must have `overflow-x: auto` wrapper for responsive
- **No file:// paths**: Never reference local filesystem in output HTML
- **Google Fonts**: Use `@import` in `<style>` (not `<link>`) for offline PDF reliability
- **All images as base64**: Embed all images inline for portability

### HTML→PDF Conversion

If Playwright is available:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{html_path}")
    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        display_header_footer=False,  # prevents path leakage
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        prefer_css_page_size=True
    )
    browser.close()
```

**Fallback (no Playwright)**: Deliver the HTML file and tell the user to open in browser → Ctrl+P → Save as PDF.

---

## §4b PDF Operations

**Library**: `pypdf`, `pdfplumber`

For working with existing PDF files (merging, extracting, watermarking).

### Merging Multiple PDFs

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter()
for pdf_path in pdf_files:
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        writer.add_page(page)
writer.write(output_path)
```

### Table Extraction

```python
import pdfplumber
import pandas as pd

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            # Process the DataFrame
```

### Watermark Overlay

```python
from pypdf import PdfReader, PdfWriter

original = PdfReader("document.pdf")
watermark = PdfReader("watermark.pdf")
writer = PdfWriter()

for page in original.pages:
    page.merge_page(watermark.pages[0])
    writer.add_page(page)
writer.write("output.pdf")
```

### Encryption

```python
writer = PdfWriter()
# ... add pages ...
writer.encrypt(user_password="read_only", owner_password="full_access")
writer.write("encrypted.pdf")
```

### Quality Checks (PDF)

- Page count matches expected
- A4 dimensions: 595 × 842 pt
- No empty pages
- Text is selectable (not screenshot/image mode)
- Logo integrity preserved

---

## §5 Flowcharts & Diagrams

Generate as inline HTML with SVG. All assets embedded as base64 — zero external dependencies.

### Shape Vocabulary

Map abstract concepts to visual shapes for consistency:

| Shape | Use For |
|-------|---------|
| Rounded rectangle (20px radius) | Start / End nodes |
| Rectangle (6px radius) | Process / Action steps |
| Diamond | Decision points |
| Circle | External actors / Users |
| Double-bordered rectangle | Subprocess / Module |
| Cylinder | Database / Storage |
| Parallelogram | Input / Output |

### Node Styling

| Element | Style |
|---------|-------|
| Process box | White fill, 1.5px primary border, 6px radius |
| Decision diamond | White fill, 1.5px primary border |
| Start/End | Primary fill, white text, rounded (20px radius) |
| Subprocess | White fill, double border in primary |

### Semantic Color Coding for Connections

| Line Color | Meaning |
|-----------|---------|
| Primary color (2px solid) | Main flow / Happy path |
| Secondary color (1.5px solid) | Trigger / Control signal |
| Functional error color (2px solid) | Error / Exception path |
| Text muted (1.5px dashed) | Async / Secondary / Optional |

### Line Rules (Critical)

- **All lines must use SVG `M` and `L` commands only** — straight segments and right-angle bends
- **Prohibited**: Bezier curves (`C`, `Q`, `S`, `T` commands), arcs, diagonal lines
- **Exception**: Loop-back arrows may use a single arc for the return bend
- Orthogonal routing: when a line needs to go around a node, use L-shaped or Z-shaped paths with right-angle folds
- Arrowheads: solid triangles, 8-10px, matching the line color

### Grid Alignment

- Snap to 120px × 80px grid
- Same row = same Y; same column = same X
- Minimum spacing between nodes: 60px edge-to-edge
- Margins: ≥ 40px on all sides
- Bounding box validation: no node overlap allowed

### Label Styling

- Font: body font, 13-14px
- Color: text.primary
- Background: semi-transparent white behind labels on lines
- No text-line overlap (offset labels if needed)
- Decision labels ("Yes"/"No") positioned near the exit point of the diamond

### Footer

- Pin to bottom of viewBox: `y = viewBox_height - 16px`
- Company logo (base64, small) + document title
- Not floating with content — fixed position

---

## §6 Branded Images

For AI-generated images (using image generation tools):

### Prompt Construction

Include these elements in every image generation prompt:
1. Brand colors as reference: "color palette includes [primary] and [secondary]"
2. Style direction matching the brand: professional/modern/bold/elegant
3. "Professional, commercial photography quality"
4. "No text, no words, no letters" (unless text is specifically requested)
5. If people are needed, specify appropriate ethnicity for the target market

### Logo Overlay

After image generation, composite the company logo onto the image:
- Position: bottom-right corner with padding (5% from edges)
- Version: white logo on dark areas, color logo on light areas (use luminance check)
- Size: logo width = 15-20% of image width
- Opacity: 90-100% (never semi-transparent)

### Output

- Format: PNG (for quality) or JPEG (for file size)
- Dimensions: specify in the generation prompt (16:9 for presentations, 1:1 for social, etc.)

---

## §7 Handbooks & Long Documents

For multi-page branded documents: employee handbooks, product manuals, training guides, company profiles.

**Method**: Paginated HTML with fixed-height A4 containers → PDF via Playwright

### Page Container System

```css
.page {
  width: 210mm;
  height: 297mm;
  overflow: hidden;   /* strict — no content spillover */
  position: relative;
  page-break-after: always;
  padding: 20mm 25mm;
  box-sizing: border-box;
}
```

Every page is a fixed 210×297mm box. Content that doesn't fit must flow to the next `.page` container.

### Content Density Estimation

Before generating, estimate page count:
- ~400-600 words per A4 page (with headings, spacing, images)
- 1000-2000 words of content → 6-8 page handbook (including cover, TOC, closing)
- Tables: ~15-20 rows per page
- Full-bleed images: 1 per page

### 10 Page Types

| Type | Layout | When to Use |
|------|--------|-------------|
| Cover | Full-bleed primary bg, centered title, logo | First page always |
| Table of Contents | Two-column with dotted leaders | After cover, if ≥ 6 pages |
| Section Divider | Primary bg, large section number + title | Between major sections |
| Content — Text | Heading + body paragraphs + optional sidebar | Standard content |
| Content — Callout | Key quote or highlight in branded box | Emphasizing a key point |
| Content — Compare | Two-column comparison layout | Before/after, pros/cons |
| Content — Cards | 2-4 card grid with icons | Features, team members, values |
| Content — Steps | Numbered vertical timeline | Processes, how-to guides |
| Content — Table | Full-width branded table | Data-heavy sections |
| Closing | CTA, contact info, logo, brand stripe | Last page always |

### Fonts for PDF

Use Google Fonts with `@import` in `<style>` to ensure fonts load in headless browser:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
```

### All Images as Base64

Every image (logo, photos, icons) must be embedded as base64 data URIs. No external file references — the HTML must be fully portable.

### Quality Checks (Handbook-Specific)

- Page count matches estimate (±1 page tolerance)
- All pages are A4 (595 × 842 pt in PDF)
- No empty pages
- No content overflow (text cut off at page bottom)
- Text is selectable in the PDF output
- Logo appears correctly on cover and closing pages
- TOC page numbers match actual content pages
