# Discovery helper: command and API contract

Standard library only; Python 3.10+ on Unix (`fcntl` advisory locking). No model calls, account access, submissions or uploads. All generated files are beneath the explicitly supplied existing workspace. No seeding is performed.

```sh
SCRIPT=/opt/data/profiles/eric/skills/research/job-discovery/scripts/discovery.py
python3 -B "$SCRIPT" --help
python3 -B "$SCRIPT" refresh --workspace /vault/eric/Research/job-search
python3 -B "$SCRIPT" refresh --workspace /vault/eric/Research/job-search --source scalable --source bjak --apply
python3 -B "$SCRIPT" report --workspace /vault/eric/Research/job-search
python3 -B "$SCRIPT" review --workspace /vault/eric/Research/job-search --key 'hays:901137/1' --decision reviewed --reason 'Human screening reason' --evidence /existing/evidence.md --application-record /existing/canonical/application.md
python3 -B -m unittest discover -s /opt/data/profiles/eric/skills/research/job-discovery/tests -v
```

CLI emits JSON. Exit 0 = successful selected automatic sources (manual/disabled/unselected are explicit skips); 1 = at least one failed/incomplete source, even when some positive observations were applied; 2 = CLI/workspace/schema/concurrency error. Inspect `sources`, not just process completion. Without `--apply`, registry bytes are untouched, but evidence, a report and the advisory lock file may be created.

Import `discovery.py` directly. Public APIs:

```python
refresh(workspace, *, apply=False, source_ids=None, fetch=None, post=None, now=None) -> dict
report(workspace) -> dict
review(workspace, *, key, decision, reason, evidence=None, application_record=None) -> dict
fetch_url(url, *, timeout=20, max_bytes=67108864, data=None, headers=None) -> bytes
post_url(url, payload, headers=None) -> bytes
```

`fetch(url)->bytes` and `post(url, payload)->bytes` permit offline evidence replay; Workday injections must also accept `headers=`; default transport issues bounded public HTTP(S) GET and JSON POST requests only (20-second socket timeout, 64 MiB per response). `now` is an ISO datetime string; default is current UTC. `review` returns the exact updated record and changes only decision/reason plus supplied evidence/application reference; existing canonical files are never opened or rewritten. Reasons must be nonempty. Decisions: `unreviewed`, `shortlisted`, `reviewed`, `excluded`, `deferred`, `applied_reported`.

## Inputs

- `sources.json`: `{ "schema_version": 1, "sources": [...] }`. Each source requires `id`, `employer`, `adapter`, `url`, `mode` (`automatic`/`manual`), boolean `enabled`, `priority` (`core`/`adjacent`), string `notes`. Source IDs use letters/digits/underscore/hyphen. Supported automatic adapter names: `ashby`, `smartrecruiters`, `greenhouse`, `personio`, `recruitee`, `successfactors`, `successfactors_json`, `workday`. Recruitee sources use the public `/api/offers` JSON feed; only observed open state codes `published` and `9` are accepted, and offers require numeric IDs, a canonical careers URL and a nonempty description. `successfactors_json` uses the public Recruiting JSON POST search and accepts an optional source `locale` (default `en_US`).
- `opportunities.json`: `{ "schema_version": 1, "opportunities": [...] }`. Required record fields: `key`, `source_id`, literal string `posting_id`, `family_key`, `employer`, `title`, `url`, string `location`, boolean `remote`, text `description`, nullable `fingerprint`, `availability`, `decision`, `reason`, nullable `application_record`, list `evidence`, `first_seen`, `last_seen`, `last_checked`. `country` is stored when supplied/explicitly inferable from Austria text. Unknown keys and manual fields survive refresh. Historical records from source IDs absent from the watchlist are valid and remain untouched.
- Personio sources must provide `role_url_template`, e.g. `https://helu.jobs.personio.com/job/{id}?language=en`, when XML lacks `<url>`. XML root must be `workzag-jobs` with `position` children. Feed language query must match the intended language.
- Greenhouse source URLs must request `jobs?content=true`; missing descriptions make the source incomplete. SmartRecruiters source URLs must start at offset 0; the helper advances offsets and fetches exact details only for preliminary candidates or already tracked IDs when summaries lack descriptions.

- Workday additionally requires observed `jobs_url` and `location_country`; `locale` defaults to `en-US` for request headers, and optional `page_size` defaults to 20 (valid 1–100). The board URL and locale must agree. Listing IDs currently must match `Req[0-9]+`; this is not a generic contract for every Workday tenant. A fresh public board token is passed in headers and redacted from the saved board response. Evidence hashes/byte counts describe the redacted bytes when `redacted: true`, not the original token-bearing response.

## Outputs and semantics

Refresh returns `events` (`key`, `kind`: `new`/`changed`/`reopened`), `review_queue` (keys excluding applied/deferred), `backlog` (all currently unreviewed keys), `sources`, `checked_at`, `applied`, `report_path`. An event on an excluded role is a reconsideration flag, never an overwritten decision or fit assertion. Events may still describe observed changes on applied/deferred roles, but these never enter `review_queue`. `report` reads the current registry and returns counts, backlog and compact unresolved rows; its `events` is deliberately empty, not a replay of earlier alerts.

Each source status includes completeness, fetched row count, errors, skip/success/partial/failure status, admitted/suppressed counts, page count where applicable, elapsed retrieval/evidence seconds, and evidence references containing request URL, method/request payload where relevant, gzip path, original byte length and SHA-256. Reports live at `runs/YYYY-MM-DD/<unique-run>/report.json`; `.raw.gz` files retain actual fetched bytes, not fabricated or summarized payloads. Large feeds must stay out of model context: inspect the compact JSON report and selected exact roles, not the raw feed.

Record additions are limited to `in_scope`/`location_review`. Tracked jobs continue updating when location changes. Explicit requisitions group families without collapsing posting/location variants. Generic remote flags never establish Austrian eligibility. Dates advertised by the employer are stored separately as `published_at`; first observation is `first_seen`. Hashes ignore publication/retrieval dates and normalized HTML/whitespace noise. A historical null hash is baseline completion, not new discovery/content-change evidence. Baseline/change/reopening adds evidence without removing existing references.

Failed/partial/malformed feeds cannot infer absence; see the empty-feed exception below. Valid positive observations from partial feeds can be applied. Absence from a validated complete nonempty feed means `not_listed`, never proof the vacancy was filled. No adapter asserts `closed` without explicit closure evidence (currently none emits it). Manual, disabled, unselected and unwatched historical sources never cause absence inference. Most adapters conservatively reject empty feeds. **Existing Workday exception:** an initial `total: 0` with `jobPostings: []` is accepted as complete and can mark tracked roles `not_listed` on `--apply`. This contradicts the conservative empty-feed policy; the code is preserved, not silently repaired. Inspect dry-run results and withhold application of an empty Workday result pending explicit completeness review. A prior nonempty dry run cannot guarantee a later mutating fetch stays nonempty. Do not treat this adapter as satisfying the empty-feed safety gate for unattended use without a separately tested correction. This never proves a role filled.

Writes use atomic replacement/fsync, a nonblocking workspace advisory lock and a pre-write byte comparison to avoid overwriting human registry edits made during collection. Workspace-escaping symlinks are rejected. Advisory locks do not prevent noncooperating writers racing the final comparison/replacement; do not concurrently hand-edit during `--apply`.

## Verification and limitations

`tests/test_discovery.py` and `tests/run_tdd.py` are retained unchanged. The historical `tdd-results.md` remains in the read-only backup, not this replacement package; it is not current validation. `run_tdd.py` appends a transcript if deliberately invoked. Tests use temporary workspaces beneath `tests/`, synthetic edge cases, and three tests require preserved evidence under `/vault/eric/Research/`. Run them on a compatible fixture layout or map those reads to the backup in an isolated local test runner. Do not modify the backup or live vault to satisfy test paths. One transport test binds loopback only.

The preserved BJAK feed contains 3156 rows and Scalable pages 110 rows; four Scalable exact descriptions are absent, so the real offline run intentionally remains incomplete while retaining the substantiated role. The Bybit exact advert uses a synthetic feed envelope. None of these historical observations establishes current live vacancies. Current test results and mapping are recorded in `../MAINTENANCE.md`.

Known limits: location triage is preliminary rather than a geographical/eligibility engine; absent/null remote flags become false (not proof of on-site work); Ashby IDs are validated as nonempty whitespace-free literal strings rather than requiring UUID format, while SR/GH/Personio IDs must be numeric. No general retry/backoff policy (SuccessFactors details have one OSError retry), scheduler, LLM fit scoring, mandatory-German inference, provider integration, or persistent re-review state beyond decisions/backlog and saved run events is added. Pagination is bounded at 1000 pages; the timeout is a socket timeout, not a hard whole-run deadline. Offline `fetch` injections are trusted byte providers. Full feeds/evidence can consume disk; no automatic evidence deletion is performed.
