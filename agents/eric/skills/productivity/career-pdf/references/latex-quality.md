# LaTeX compilation and quality checks

Use this reference for the Stage 2 production of an approved career-document Markdown file. It governs compilation and artifact verification; `cv-writing` owns content and career evidence.

## Build

Use the approved builder and frozen template release. Read the template README and invoke the release builder with `--draft` pointing to the frozen revision copy and `--output` to a new artifact basename. The builder already compiles and checks its output; do not add redundant compilation merely because an example command appears below. Validate supported Markdown without modifying it. Record the release identity/hashes and approval state alongside input/artifact hashes. Do not overwrite a delivered or submitted artifact. Compile with shell escape disabled and fail on errors:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
  -output-directory=OUTPUT_DIR INPUT.tex
```

Compile again only when the builder requires it. Keep optional page breaks and other supported layout options revision-local; never add employer-specific branches to the shared builder. A lasting template change needs a separately approved new release, not edits to a frozen release. Keep the editable `.tex`, PDF, compiler log, build options and concise verification record in the same revision directory.

Do not install software, change installed packages, upload private material, change shared template releases, or alter reviewed wording without explicit permission.

## Required checks

- Confirm the final PDF exists at the requested path and has the intended page count.
- Inspect the compiler log. A non-zero exit, missing character, incorrect extracted character, or unresolved overfull/underfull box warning is a failed build.
- Extract text page by page. Check names, contacts, dates, headings, employers, roles, skills, requested omissions and unexpected control characters.
- Compare the extracted text with the frozen Markdown closely enough to catch missing or altered content. Treat known headers, footers, whitespace and discretionary hyphenation carefully; do not broadly strip text to make a check pass.
- Check factual fields in the generated TeX against the frozen Markdown. Technical success does not authorise a content change.

Use the generic `pdf` skill’s selective verification reference/helpers for extraction and page rendering; do not load its general creation or installation procedures. Before visual review, check whether `pypdfium2` imports or `pdftoppm` is available. If neither is available, do not invoke rendering helpers, retry alternatives, install software or upload the PDF. Report that visual inspection was unavailable. If a renderer is available, inspect every page for clipping, wrapping, spacing, page breaks and heading/bullet continuity. Inspect `pdf_page_image.py` JSON: exit 0 with `rendered: false` means unavailable; only `rendered: true` and actual page images establish rendering. Rendering itself is not visual approval.

## Bounded recovery

Diagnose the actual failure before another build. A compilation, glyph, horizontal-overflow and page-break problem require different remedies.

Use only the smallest revision-local correction that preserves the frozen Markdown, approved typography, margins and template release. Record it in the revision. If the remedy changes content, return to Stage 1 for Markdown revision and renewed approval. Typography, margin or shared-template changes require separately scoped production/presentation review with Rob; they do not belong to CV editorial work. For a page target, first test the approved content with approved layout; never silently cut unrelated prose or shrink type/margins. Do not use blanket warning suppression such as `\sloppy`.

Do not add incident-specific fixes to this reference. Record any candidate improvement separately for deliberate maintenance review.


Text extraction and appearance are separate checks. Never switch an isolated name or acronym to a code font to satisfy an extractor. After an authorised font correction, verify actual affected PDF text runs and appearance; a removed source command or parser-inferred spacing is insufficient. Read-only formatting questions do not authorise changes or another build. No check here establishes universal ATS compatibility.
