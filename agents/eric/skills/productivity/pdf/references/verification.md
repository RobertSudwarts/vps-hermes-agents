# PDF operation checks

Use an existing interpreter with the specific helper's dependencies. The core
helpers use pypdf, reportlab and/or pdfplumber; rendering also needs Pillow and
pypdfium2 or installed `pdftoppm`. Check capability, not just executable names.
Do not follow install hints automatically. [Commands](commands.md) lists CLIs;
inspect `--help` for exact flags and outputs. Not every helper emits the same schema.

## Inspect and extract

- Inspect metadata, encryption, page count and scanned-page indicators with
  `pdf_read.py --meta`. Use authorised passwords as needed; preserve originals.
- Extract selected text/tables/fields; check known strings and literal values,
  non-ASCII content, dates and reading order. Empty text from a scanned page does
  not mean no content: use [OCR/extraction](ocr-extraction.md).
- Table extraction is heuristic; merged/borderless tables may need tuning or
  explicit uncertainty. Do not manufacture missing cells or treat OCR as verified
  source wording without checking the page.

## Render and inspect

`pdf_page_image.py` takes **1-based** page ranges. `_raster.py` is its shared
backend module, not a CLI. It selects pypdfium2 then pdftoppm when available;
backend errors can still fail rather than automatically recover.

Inspect returned JSON: `rendered: true` plus existing image files establishes
rendering, not visual approval. `rendered: false` with exit 0 means unavailable.
For form overlays, inspect the nested `overlay.rendered` value. A blank-page
layout overlay does not prove appearance of the actual filled PDF.

Review every relevant page for clipping, overlaps, glyphs, wrapping, page breaks
and heading/bullet continuity. Do not introduce code fonts or alter hierarchy to
appease one extractor. After an authorised font correction, inspect the affected
PDF text runs and appearance, not merely the removed source command. Parser spaces
inside acronyms alone do not justify a design change. State any unavailable check.

## Check by operation

- **Create/merge/split/rotate:** expected pages/order, retained text and requested
  rotation. CLI page ranges are generally 1-based; do not double-convert pypdf's
  0-based API indices. Rotation must be a multiple of 90. Compression deflates
  streams; it does not promise substantial savings or downsample images.
- **Forms:** lint layout before building. Re-read exact field names/types/options
  and values after filling; verify non-ASCII values and rendered appearance.
  Stored text can round-trip while a font lacks glyphs. Appearance regeneration
  differs by viewer. Flattening may misrender custom widgets/radio groups; inspect
  output visually and preserve the unflattened source. Do not silently rasterise
  as a repair: that changes selectable text and interactive properties.
- **Stamps/watermarks:** verify content, placement, opacity and selected pages.
  Rotated text may confuse pdfplumber; use pypdf extraction or rendered images.
- **Metadata/attachments:** re-read metadata/listing and byte-compare extracted
  attachments. Classic DocInfo edits do not change embedded XMP automatically.
- **Encryption/decryption:** confirm encrypted state and refusal without a valid
  password; decrypted output should retain original content. Permission flags
  are viewer requests, not access security. Keep passwords out of saved reports.
- **PDF/A:** these utilities do not establish conformance. Conversion and validation
  require separately available appropriate tools and checks; do not assume success
  or install them implicitly.

Report artifact paths, relevant checks, failures and limits concisely. Local
creation is not delivery to an employer, submission or ATS certification.
