# Stable citations and evidence

## Existing helper contract

`scripts/sources.py` is standard-library Python. Ledger resolution is:
`--ledger PATH`, then `HERMES_CITATION_LEDGER`, then
`get_hermes_home()/cache/citations/ledger.json`. `_hermes_home.py` uses Hermes'
resolver when available, otherwise `HERMES_HOME` or `~/.hermes`.

Prefer an explicit task ledger beside the existing research evidence. A new path
starts empty automatically. `reset` overwrites the chosen ledger: use only for an
intentionally new/disposable task, never for continued or cited work. Do not reset
a shared profile ledger merely because a new question arrives. The v1 JSON schema
is `{version: 1, sources: [...]}`; entries carry stable `id`, normalized `url`,
`title`, `accessed`, and optional `quotes` with `text`/`added`.

`add` is idempotent within one ledger: it removes URL fragments/trailing slashes
but preserves query strings. It neither fetches nor validates the URL. `ingest`
walks JSON `url`/`link`/`source_url` fields; inspect retrieved content before treating
these as support. Keep discovery-only/failed leads labelled in retrieval notes.
Atomic replacement and the helper's best-effort lock are not a transaction system;
serialize ledger writes where practical. If authorised parallel research is merged,
use one explicit ledger/registration owner, not colliding per-worker IDs.

## Retrieve, cite, render, verify

Use the installed skill path on Hermes; in local checks resolve this package's
`scripts/sources.py`. Put the global `--ledger` argument before the subcommand.

```sh
CITE_HELPER=/opt/data/profiles/eric/skills/research/grounded-citations/scripts/sources.py
CITE_LEDGER=/vault/eric/Research/<topic>/ledger.json
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" --help
```

After actual retrieval, use `add URL --title TITLE --accessed YYYY-MM-DD` (or
`ingest results.json`) and keep the returned IDs. `list --json` inspects the ledger;
filter selected entries rather than repeatedly dumping it.

Compose supported sentences with IDs immediately after punctuation: `Claim.[1][2]`.
Use separate brackets, no more than three IDs per sentence; cite while writing,
not by retrofitting plausible sources later. Preserve exact names, figures, dates
and units. Attribute conflicting readings separately. Explicitly mark unresolved
load-bearing claims `[unverified]`; do not use that marker instead of available
research or pass it off as verification.

```sh
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" render --replace-in report.md
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" verify report.md
```

`--replace-in` rewrites from the last Sources heading onward: keep Sources last
and use only a mutable current draft. `render --cited-in report.md` prints without
editing; `--only 1,3` selects IDs for short chat answers. Do not retype source
mappings or renumber IDs. Normal verification returns 1 on errors; `--strict`
also fails warnings, including uncited registered leads. Explain unused-lead
warnings rather than padding prose with irrelevant citations. Malformed input or
CLI/file errors can return 2 or other nonzero status: inspect the diagnostic.

## Evidence-backed claims

For requested fact-checking, disputed or high-stakes claims, attach substantive
claim-bearing excerpts from saved retrieved page text:

```sh
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" quote 1 --text 'exact supporting words' --from evidence/page.txt
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" render --style evidence --replace-in report.md
python3 -B "$CITE_HELPER" --ledger "$CITE_LEDGER" verify report.md --evidence
```

`quote` requires at least three words and checks literal presence ignoring case,
whitespace and Markdown markup. It rejects paraphrases; use actual source text,
not a search snippet or generic heading chosen to pass. Respect quotation limits
in delivered output. `--evidence` checks at least one quote per cited source, not
support for every claim or authenticity of the supplied evidence file. Check each
claim's entailment, scope and date yourself. Corroborate disputed facts with an
independent source; mirrors of one announcement are not independent evidence.

Optional `--min-coverage 0.5` measures declared provenance, not truth: `[n]` and
`[unverified]` both count. It uses a rough split of 4+-word prose fragments, excluding
headings, tables and fenced code; inspect stats before choosing a threshold.
Read warnings even on success. Never weaken a claim or fabricate a quote merely
to make a check green. Formatting variations use [citation formats](citation-formats.md).
