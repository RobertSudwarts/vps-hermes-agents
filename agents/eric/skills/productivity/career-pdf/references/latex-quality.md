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

## Required automated checks

- Confirm the final PDF exists at the requested path and has the intended page count.
- Inspect the compiler log. A non-zero exit, missing character, incorrect extracted character, or unresolved overfull/underfull box warning is a failed build.
- Extract text page by page. Check names, contacts, dates, headings, employers, roles, skills, requested omissions and unexpected control characters.
- Compare the extracted text with the frozen Markdown closely enough to catch missing or altered content. Treat known headers, footers, whitespace and discretionary hyphenation carefully; do not broadly strip text to make a check pass.
- Check factual fields in the generated TeX against the frozen Markdown. Technical success does not authorise a content change.

## Visual review and delivery gate

For routine builds from approved Markdown using the unchanged approved frozen
template and supported existing layout options, passing all automated checks
above is sufficient for delivery. A missing renderer is not a failed build and
must not block delivery, trigger another approval request or repeated attempts
to install/find tools. Preserve the frozen text and record visual inspection as
not performed. Compilation alone is insufficient; text fidelity, clean glyph/
layout checks and the requested page count still must pass. Do not ignore a known
visual defect merely because automated checks pass.

Use the generic `pdf` verification helpers selectively. Check existing rendering
capability once when unknown; reuse a known unavailable result unless the
environment changes. If available, render and inspect every page for clipping,
wrapping, spacing, page breaks and heading/bullet continuity. Inspect helper JSON:
exit 0 with `rendered: false` means unavailable; `rendered: true` and actual images
establish rendering, not visual approval. If rendering fails, record the actual
failure; for an otherwise passing routine build, deliver with that limitation
rather than retrying indefinitely or changing software/uploading the PDF.

New/changed templates, typography, margins or unfamiliar layout corrections
require visual review before presentation approval. Supported options within the
unchanged approved builder, such as an existing page-break option, do not by
themselves create a new template. If a change requires visual review and local
rendering is unavailable, provide a clearly labelled review candidate for Rob's
inspection; do not mark the presentation approved or the visual check passed.
Separately scoped presentation changes still require Rob's authority.

Keep routine delivery concise, for example: “PDF ready. Compilation, text fidelity
and page-count checks passed. Visual inspection wasn't available.” Mention the
limitation once with the delivered artifact; do not repeatedly warn about the
same missing renderer. Record detailed check results in the revision, not chat.

## Bounded recovery

Diagnose the actual failure before another build. A compilation, glyph, horizontal-overflow and page-break problem require different remedies.

Use only the smallest revision-local correction that preserves the frozen Markdown, approved typography, margins and template release. Record it in the revision. If the remedy changes content, return to Stage 1 for Markdown revision and renewed approval. Typography, margin or shared-template changes require separately scoped production/presentation review with Rob; they do not belong to CV editorial work. For a page target, first test the approved content with approved layout; never silently cut unrelated prose or shrink type/margins. Do not use blanket warning suppression such as `\sloppy`.

Do not add incident-specific fixes to this reference. Record any candidate improvement separately for deliberate maintenance review.


Text extraction and appearance are separate checks. Never switch an isolated name or acronym to a code font to satisfy an extractor. After an authorised font correction, verify actual affected PDF text runs and appearance; a removed source command or parser-inferred spacing is insufficient. Read-only formatting questions do not authorise changes or another build. No check here establishes universal ATS compatibility.
