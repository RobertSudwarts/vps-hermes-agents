---
name: pdf
description: Read, extract, create and manipulate PDFs, fill forms and render pages. CV production belongs to career-pdf; editing career wording belongs to the relevant writing skill.
version: 2.0.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pdf, documents, forms, ocr, text-extraction, reportlab, pypdf]
    category: productivity
    related_skills: [career-pdf, cv-writing, cover-letter-writing, grounded-citations]
---

# PDF utilities

Provide document mechanics, not career editorial policy. Reading an existing CV
PDF is ordinary extraction; do not load career methodology for that task.
CV drafting/revision belongs to `cv-writing`; approved CV production to
`career-pdf`; letters and their approved production to `cover-letter-writing`.
Never bypass their text-approval gates by creating or editing a career PDF here.

## Select only the relevant reference

- Helper CLI or general creation/manipulation: [commands](references/commands.md).
- Extraction, rendering and operation-specific checks: [verification](references/verification.md).
- AcroForm design/filling: [forms](references/forms.md), plus the applicable verification checks.
- Scans or incomplete text extraction: [OCR/extraction](references/ocr-extraction.md).
- Requested natural-language editing of a non-career PDF: [editing boundaries](references/nano-pdf-editing.md).
- Non-career LaTeX production: [LaTeX checks](references/latex-quality.md). CVs use career-pdf's own production reference instead.

## Preserve scope and report actual results

Use already installed tools; check imports/help read-only before choosing an
interpreter. Do not install, upgrade, remove or configure software, build an
environment, download model weights or enable external processing without
explicit permission for that separate action. Script install hints are diagnostics.
Never upload private documents merely because local extraction/rendering failed.

Preserve inputs and existing delivered/frozen artifacts; write a distinct output.
A read-only question does not authorise edits or compilation. No submission,
outreach, configuration changes or automatic skill mutation follows from PDF work.

Check actual outputs, not only exit status. Rendering can return exit 0 with
`rendered: false`; report visual inspection unavailable, not passed. Inspect all
relevant rendered pages when available. For routine approved-template CV builds, follow `career-pdf`’s delivery gate:
missing rendering alone does not block delivery after its automated checks pass.
This does not waive visual checks for presentation changes or unrelated PDF tasks.
Text extraction and appearance are separate
checks; never degrade typography or silently change wording to satisfy a parser.
Keep bulk extracted text/logs on disk and return selected results and limitations.
