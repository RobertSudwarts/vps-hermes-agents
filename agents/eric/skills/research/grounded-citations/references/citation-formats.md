# Citation output formats

The ledger owns stable IDs/URLs. Render mechanically; do not type a Sources block
from memory. Verify the numbered Markdown research source before conversion and
check the resulting document separately: the helper does not parse DOCX/PDF,
BibTeX citations or Markdown footnote references as equivalent `[n]` citations.

| Target | Representation |
|---|---|
| Markdown/chat research | Sentence-level `[n]`; `render --cited-in draft.md` or `--style plain --only 1,3` for a short answer |
| Obsidian/multiple pages | One ledger shared across the task; per-page Sources blocks, no resets between pages |
| Footnote-oriented documents | `--style footnotes` emits Markdown definitions `[^n]: URL`; a separate document tool must convert these while preserving mapping |
| Bibliography-oriented research | `--style bibtex` emits `@misc` entries keyed `sourceN`; venue formatting/compilation needs a separate appropriate workflow |
| Slides | Mark claim-bearing bullets and place the rendered source list in the agreed notes/final slide |
| Spreadsheets | Stable source-ID column plus a source sheet generated from the ledger |
| Evidence report | `--style evidence` adds attached quotations; inspect relevance and respect quotation limits |

Use one citation system per output. Keep Sources last in mutable Markdown drafts
because `--replace-in` replaces everything from the last Sources heading onward.
No ad hoc code-comment citations or unsupported dependencies. Research provenance
for employer-facing CVs/letters belongs in separate evidence notes; citation
formatting does not authorise adding content to an approved document or building
it. `career-pdf` owns CV production after approval and an explicit PDF request.
