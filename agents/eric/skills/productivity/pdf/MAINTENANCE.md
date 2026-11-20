# PDF package migration and validation

Local revision only. The backup at
`/data/vps-agent-backups/eric/profile/skills/productivity/pdf/` was read-only;
no live profile, software environment or template release was modified.

## Original-file mapping

| Original | Disposition |
|---|---|
| `SKILL.md` | Compact generic utility router. CLI catalogue moved to `references/commands.md`, operation checks to `references/verification.md`; career production handed to career-pdf. Automatic environment/setup recipes omitted. |
| `references/forms.md` | Existing specification retained; clarified that rendering hints are diagnostic and `overlay.rendered` must be checked. |
| `references/ocr-extraction.md` | Rewritten for selective local/public extraction, explicit privacy/model-download boundaries and correct page-index conventions. Removed installation recipes, unrelated arXiv examples and duplicate manipulation snippets. |
| `references/nano-pdf-editing.md` | Rewritten as optional non-career editing only, with confirmed page indexing, separate output, data-flow checks and content/visual verification. No guessed page retries or implicit installation. |
| `references/latex-quality.md` | Reduced to generic non-career compilation/checks. Career-specific preservation, layout and presentation safeguards moved into career-pdf's reference. |
| `references/latex-quality.md.bak` | Not carried into replacement: historical duplicate, not an active authority. Backup remains untouched. |
| `tests/test_pdf_skill.py` | Retained byte-for-byte. |
| `LICENSE` | Retained byte-for-byte. |
| `scripts/_raster.py` | Retained byte-for-byte |
| `scripts/extract_marker.py` | Retained byte-for-byte |
| `scripts/extract_pymupdf.py` | Retained byte-for-byte |
| `scripts/pdf_create.py` | Retained byte-for-byte |
| `scripts/pdf_fill_form.py` | Retained byte-for-byte |
| `scripts/pdf_form_layout.py` | Retained byte-for-byte |
| `scripts/pdf_make_form.py` | Retained byte-for-byte |
| `scripts/pdf_merge.py` | Retained byte-for-byte |
| `scripts/pdf_meta.py` | Retained byte-for-byte |
| `scripts/pdf_page_image.py` | Retained byte-for-byte |
| `scripts/pdf_read.py` | Retained byte-for-byte |
| `scripts/pdf_secure.py` | Local repair: replace invalid `***` placeholders with the existing argparse password attributes; CLI unchanged |
| `scripts/pdf_split.py` | Retained byte-for-byte |
| `scripts/pdf_stamp.py` | Retained byte-for-byte |
| `scripts/pdf_watermark.py` | Retained byte-for-byte |

New references are `commands.md` and `verification.md`; this maintenance map is
not routine task context. Helper install hints still describe old setup routes;
the revised instructions explicitly treat them as diagnostics, never authority
to install. Executable behaviour is unchanged except the documented syntax repair.

## Consequential local changes

- `cv-writing/references/markdown-format.md`: new small output contract verified
  against frozen ModernCV v003; linked from substantive drafting before approval.
- `career-pdf/SKILL.md` and `references/latex-quality.md`: use the hash-verified
  frozen copy as build input, validate structure without repair, preserve release
  identity, manifest and layout exceptions, separate content from presentation
  review, and check rendering JSON/actual appearance. v004 stays a candidate.
- `cover-letter-writing/SKILL.md` and `references/letter-pdf.md`: selective generic
  utility dependency; explicit rendering-result checks and no direct PDF text edits.
- `grounded-citations/SKILL.md` and `references/public-ats-recovery.md`: extraction
  handoff only; research keeps URL/date/page provenance and citation ownership.
- `skills/README.md`: six-package inventory and aligned adoption guidance replacing
  the obsolete prohibition on revising generic PDF instructions.
- `agents/eric/workflow-design.md`: short statement of generic utility ownership
  and missing-renderer boundaries, without duplicate production methodology.

## Validation

Existing PDF suite: 22 tests initially passed; encryption failed because the
original backup script contained invalid `***` syntax. The two argument references
were restored only in the local copy and the encryption round-trip then passed.
Thus all 23 existing tests passed across the initial run and targeted repair run.
Tests used synthetic PDFs and temporary directories; no private career material,
network access or installation. The existing bundled document runtime and cached
pytest modules were used process-locally, without environment configuration changes.

A synthetic four-section Markdown fixture parsed through the read-only frozen
v003 builder, including full-address header, skill labels, role metadata and
selected-history prose; an unsupported heading was rejected. No compiler or
historical document build was run. Template releases remain unchanged.

All other 14 helper files, the original test file and licence were compared
byte-for-byte to the backup. Link, YAML, Python syntax and whitespace checks apply
to the revised package and affected skills. Generic Codex skill validation rejects
the retained Hermes metadata keys (`version`, `author`, `platforms`); these are
intentional schema differences, not missing YAML fields.
