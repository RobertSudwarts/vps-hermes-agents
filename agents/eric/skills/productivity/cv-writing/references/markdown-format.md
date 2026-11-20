# CV Markdown contract for the approved builder

Use when creating or restructuring a CV, before Rob approves it. This is an
output-format contract, not a PDF procedure. The approved ModernCV v003 builder
accepts a small Markdown subset; it is not a general Markdown renderer.

- First block: exactly two lines, `# Full Name` then
  `Full address · phone · email`, using confirmed contact values. Do not invent
  an address or replace a deliberately requested omission without review.
- Four section headings, each in its own blank-line-separated block, exactly:
  `## About me`, `## Skills`, `## Experience`, `## Education`, in that order.
- Skills are bullets: `- **Label:** description`.
- Each experience heading block has exactly two lines:
  `### Employer — Role` then `**Location · Dates**`. Separate narrative/bullets
  from that block with a blank line. Preserve factual titles and chronology.
- Use plain paragraphs, `- ` bullet lists and paired inline `**bold**`.
  Indented continuation lines extend a bullet. Avoid tables, nested lists,
  embedded images, raw LaTeX, links or other Markdown syntax the builder does
  not interpret. Education remains concise factual prose/bullets.

Blank lines separate blocks, not every line within a role header or bullet list.
Keep private evidence/uncertainty notes outside `cv.md`. If selected-history
labelling is needed, use a brief paragraph under Experience, not another heading.

Check this structure while drafting and show the resulting exact saved file for
approval. A user-requested different structure may need a separately reviewed
renderer change; do not quietly override the request. If an already approved
file is incompatible, return the precise issue for review rather than silently
reformatting or changing its content during production. The frozen template's
README and builder remain authoritative for supported syntax; do not modify them
as part of CV drafting. A newer candidate release is not automatically approved.
