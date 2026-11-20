# LaTeX compilation and quality checks

Use this reference for the Stage 2 production of an approved career-document Markdown file. It governs compilation and artifact verification; `cv-writing` owns content and career evidence.

## Build

Use the approved builder and frozen template release. Do not overwrite a delivered or submitted artifact. Compile with shell escape disabled and fail on errors:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
  -output-directory=OUTPUT_DIR INPUT.tex
```

Compile again when the builder requires it. Keep the editable `.tex`, PDF, compiler log, build options and concise verification record in the same revision directory.

Do not install software, change installed packages, upload private material, change shared template releases, or alter reviewed wording without explicit permission.

## Required checks

- Confirm the final PDF exists at the requested path and has the intended page count.
- Inspect the compiler log. A non-zero exit, missing character, incorrect extracted character, or unresolved overfull/underfull box warning is a failed build.
- Extract text page by page. Check names, contacts, dates, headings, employers, roles, skills, requested omissions and unexpected control characters.
- Compare the extracted text with the frozen Markdown closely enough to catch missing or altered content. Treat known headers, footers, whitespace and discretionary hyphenation carefully; do not broadly strip text to make a check pass.
- Check factual fields in the generated TeX against the frozen Markdown. Technical success does not authorise a content change.

Before visual review, check whether `pypdfium2` imports or `pdftoppm` is available. If neither is available, do not invoke rendering helpers, retry alternatives, install software or upload the PDF. Report that visual inspection was unavailable. If a renderer is available, inspect every page for clipping, wrapping, spacing, page breaks and heading/bullet continuity.

## Bounded recovery

Diagnose the actual failure before another build. A compilation, glyph, horizontal-overflow and page-break problem require different remedies.

Use only the smallest revision-local correction that preserves the frozen Markdown, approved typography, margins and template release. Record it in the revision. If the remedy requires a content, template, font-size or margin change, stop and return to Stage 1 for review.

Do not add incident-specific fixes to this reference. Record any candidate improvement separately for deliberate maintenance review.

