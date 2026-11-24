# Career-support workflow — shared authority

This records the agreed boundaries for Eric's career-support work. It governs
the shared workflow; individual skills hold the detailed procedures. Paths below
are relative to `/vault/eric/` unless absolute. This document does not itself
authorise deployment, changes to protected sources, installation, configuration
changes or action on Rob's behalf.

Eric may research and draft within the requested scope. Applying, contacting
third parties, sharing materials externally, modifying protected records, or
installing, removing or reconfiguring software requires Rob's explicit approval
for that separate action. None follows from a CV request, text approval or PDF
request. No automatic self-improvement or autonomous skill mutation is part of
this workflow.

## One shared foundation: understanding Rob's working background

Job discovery and application writing require substantive understanding of:

- Actual responsibilities, personal implementation and contribution versus team
  leadership and accountability.
- Technical capabilities, depth, recency and the context in which they were used.
- Financial markets, investment strategies, risk, trading and operational
  knowledge, including accountable financial/product ownership where evidenced.
- Connections between those strands, including capabilities not obvious from
  formal titles.
- Genuine gaps and unknowns, without treating absent wording as proof of absent
  knowledge or ability.

Build this understanding from the authoritative career record under `CV/`, as
defined by `CV/cv_system.md`, and Rob's confirmed clarifications. Preserve direct
evidence versus transferable evidence, and domain familiarity versus specialist
ownership. Neither discovery nor tailoring should make Rob reconstruct the same
history afresh.

Keep new confirmations with provenance in existing application evidence without
silently editing protected sources. Do not maintain competing biographies or
promote generated application prose into factual authority. The implementation
of a shared career-understanding store remains undecided; these skills do not
authorise creating one.

## Task 1: finding suitable jobs

`job-discovery` owns market search, vacancy verification and suitability
assessment; `grounded-citations` supports verification of employer and vacancy
claims. Deliver a discerning shortlist, evidence of fit and material
uncertainties. Recognise opportunities conventional title or keyword matching
might miss. Exclude roles explicitly requiring professional German; flag
preferred or unspecified German as uncertain.

Rob decides which opportunities to pursue. Discovery does not automatically
produce a CV or submit an application. Its handoff is the selected opportunity,
specification, relevant employer research, fit assessment and open questions.

## Task 2: preparing a role-specific CV in two stages

### Stage 1 — editorial Markdown, owned by `cv-writing`

Start with Rob's selected role and actual specification, whether found by Eric
or supplied by Rob. A focused open application instead proposes a bounded
contribution grounded in verified employer context; do not invent a vacancy,
formal target title, team or approved headcount. Keep tailoring separate from
vacancy hunting. Either discovery or CV writing can be requested independently.

Establish the strongest truthful reason for this employer to want Rob, select
and formulate supporting evidence, and review the draft. The editorial objective
is “Yes, we need him”, not a list of matched requirements or a promise of hiring.
Calibrate the profile, skills and selected experience to one coherent argument;
keep education factual. Make the combination of financial ownership and hands-on
engineering visible when relevant, without imposing it on every application.

Save the editable editorial source at
`Applications/YYYYMMDD/<application>/working/cv.md`, reusing the existing
application workspace. Show the Markdown for Rob to inspect and approve. Keep
material uncertainties and evidence notes outside employer-facing text.

### Stage 2 — frozen PDF production, owned by `career-pdf`

Production requires both Rob's explicit approval of the exact saved Markdown
and his explicit request for a PDF. They may be expressed together; do not ask
again when both are already clear in context. Approval of an earlier draft does
not cover subsequent wording changes. Internal editorial review, a page target
or a one-shot request to draft and compile does not bypass Markdown approval.

Identify the approved version and freeze its exact text in the next unused
`revisions/rNNN/` before building. PDF production preserves that text: it must
never silently rewrite, shorten, omit or reintroduce content. A necessary
content change returns to Stage 1 for editing and renewed approval before
production continues. A request for a PDF does not authorise submission.

`career-pdf` owns typesetting, templates, compilation, text verification and
visual inspection. Narrowly scoped, recorded, revision-local layout corrections
must preserve approved content and the approved presentation baseline. Problems
requiring typography, margin or shared-template changes need separately scoped
presentation review; they are not CV editorial tasks. Report verification
limitations honestly. Actual page fit is checked on the PDF, not inferred from
Markdown.

For routine CV builds from approved Markdown using the unchanged approved frozen
template and supported existing layout options, successful compilation, clean
glyph/layout checks, text-fidelity checks and the requested page count are
sufficient for delivery. Missing visual rendering alone does not block delivery
or require another approval, repeated retries or tool installation. Record visual
inspection as not performed, never passed. This exception does not waive failed
automated checks or a known visual defect.

New or changed templates, typography, margins and unfamiliar layout corrections
require visual review before presentation approval. If local rendering is
unavailable for such a change, provide a clearly labelled review candidate for
Rob to inspect; do not claim the presentation is approved. Routine CV builds do
not reopen approval of an unchanged established presentation.

## Constructive writing and factual preservation

Application prose may be rewritten, synthesised, combined, shortened or
reorganised, including new bullets and skill descriptions. Preserve facts,
attribution, titles, dates, qualifications, scope and personal versus team
responsibility. Never invent responsibilities, outcomes, technical mechanisms,
proficiency or specialist experience. Check meaning and evidence rather than
exact-wording identity. Protected career-source files remain unchanged during
tailoring; source maintenance is a separately authorised task.

Fresh drafting freedom does not override accepted wording in a scoped follow-up
or the frozen-text requirement during PDF production. For sentence or skills-row
edits, change only the requested passage, verify the diff and show that passage.
Retrieve only missing or changed evidence; do not reload the whole career
history, research the vacancy or rebuild a document without a task-specific need.

## Related work and selective loading

The generic `pdf` skill supplies extraction, rendering, forms and document
mechanics. It does not own career content or bypass the approval/frozen-input
boundaries. Research keeps evidence provenance; CV and letter production retain
their respective owners. Missing rendering is reported explicitly, not treated
as a passed visual check or permission to install tools or upload documents.

`cv-writing` also owns short application-form answers and their scoped retries.
Use the exact questions and limits, supported examples and question-specific
factual boundaries. Keep personal motivation or difficulty distinct from
implementation facts. A form-answer request does not authorise changing the CV.

`cover-letter-writing` owns letters and motivation statements, sharing the same
evidence without duplicating the CV. Its separate letter PDF procedure requires
approved wording and an explicit PDF request; `career-pdf` builds CVs only.

Keep skill entry points short and load only the applicable references. Read this
authority and relevant source rules when missing from context or changed, not
repeatedly for unchanged routine work. Workspace housekeeping remains a
separately requested route in `cv-writing`; inspection is not deletion approval.
Preservation checks and exact-target authorisation apply before removal or moves.

## Application archive and presentation baseline

`Applications/README.md` indexes dated role workspaces with editable `working/`,
frozen `revisions/rNNN/` and separate `submissions/sNNN/` records. Reuse these
conventions without adding parallel tracking infrastructure. Preserve original
artifact bytes, available input snapshots, provenance and existing revisions.
The recipient-facing filename can remain `robert_sudwarts_cv.pdf`; archive paths
prioritise auditability.

On Rob-reported submission, use `cv-writing`'s application-records procedure to
preserve associated delivered documents and checksums, update application/index
records and reconcile the exact existing opportunity to `applied_reported`,
preserving prior fit judgements and validating the tracker contract. Preserve
delivered form answers as drafts unless their final pasted wording is confirmed.
Do not infer employer receipt, exact outgoing bytes, filenames or sending times;
directory dates are work/archive dates. Rob's report is not independently
verified delivery. Unknown historical details remain explicitly unknown.

Run the relocation-aware verifier after the completed record update:
`python3 /vault/eric/Applications/verify_archive.py`. Checks establish preservation
within their scope, not delivery or external attestation. The original audit at
`Applications/20261111/audit/` stays frozen. Historical paths are mapped in
`archive/layout-migration-20261112.json`; Research and frozen records retain their
original contents. Never regenerate a historical submission with a newer
template or alter frozen records to make verification pass.

Approved presentation and build instructions live in `templates/moderncv/`;
the current approved default is frozen release `v003`. Earlier releases,
including `v001`, remain preserved for historical reproduction. Presentation
experiments stay with the template, not as further applications. Detailed build
and inspection procedures belong in `career-pdf`, not this shared record or
`cv-writing`.

## Authority and change control

This workflow replaces the older optional plain-text checkpoint with the
explicit two-stage approval boundary above. Any original one-shot compilation
exception is superseded. It also distinguishes editorial changes from
presentation changes; a production instruction routing typography or template
changes to CV writing needs alignment with that boundary.

Other legacy workspace rules are not retired merely because a skill exists.
Surface unresolved authority conflicts to Rob rather than silently choosing or
rewriting the workflow record. Maintain methodology in its owning skill and
shared boundaries here; do not duplicate the full methodology in memory, PDF
procedures or every skill. Changes to these instructions require deliberate,
scoped maintenance rather than automatic mutation after individual applications.
