# Selective PDF extraction and OCR

First distinguish a public source from private/local material. For a public PDF,
use an available permitted retrieval route and preserve original bytes, URL and
date. Do not force a remote extraction service when it is unavailable or search-only.
Private CVs, letters and career records stay local unless external processing was
explicitly authorised. A URL does not by itself make a document public.

Inspect the text layer first. Use `pdf_read.py` for ordinary PDF text/tables;
`extract_pymupdf.py` is an optional existing-tool path for text, Markdown, tables,
images and metadata. Read its help: its `--pages` uses **0-based** ranges, unlike
`pdf_page_image.py`'s 1-based CLI. Inspect only missing/relevant pages when possible.
For a few scanned pages, render with available local tools and use an authorised
image-reading route; do not assume any remote vision route is private/local.

For bulk OCR, `extract_marker.py` is retained as an optional helper. Before use,
check that dependencies and model weights already exist and that the chosen mode
will not trigger downloads or external calls. Installed Python packages alone do
not establish readiness: model initialization may download weights. `--check`
reports capacity, not proof that all models are cached. No environment creation,
package installation or first-use model download without separate permission.

`--use_llm` may enable external processing depending on configuration. Do not use
it for private material without verifying data flow and obtaining explicit
permission. If local OCR is unavailable, report the specific limitation; do not
substitute an automatic upload or claim text-only extraction covered image pages.

Preserve page association and originals. Verify names, figures, dates, units and
relevant tables against the rendered source. Label uncertain OCR characters;
never silently correct them from expected meaning. For research, return source
and page mapping to `grounded-citations`, which owns citations and claim support.
No CV production or career-source update is authorised by extraction.
