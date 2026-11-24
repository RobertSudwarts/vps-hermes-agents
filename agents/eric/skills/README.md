# Eric's focused career skills

This is a proposed replacement for Eric's career workflow layer. It is deliberately separate from the generic Hermes skills currently installed on the VPS.

## Scope

The set contains five career workflow skills plus the revised generic PDF utility:

- `job-discovery` — find, assess and track opportunities.
- `grounded-citations` — verify external claims and retain evidence.
- `cv-writing` — prepare a tailored Markdown CV for review.
- `cover-letter-writing` — prepare a separate, role-specific letter.
- `career-pdf` — turn an explicitly approved Markdown CV into a frozen PDF revision.
- `pdf` — general extraction, rendering, forms and PDF manipulation; it does not own career editorial work or bypass approval.

The protected career record remains under `/vault/eric/CV/`; these skills must never modify it while tailoring. `/vault/eric/workflow-design.md` is the shared durable workflow policy.

## CV hand-off

`cv-writing` is Stage 1: it creates or revises `working/cv.md`. It does not build a PDF.

`career-pdf` is Stage 2: it runs only when Rob explicitly asks to build the approved Markdown. It copies that exact file into `revisions/rNNN/` before compiling. It may make recorded, revision-local layout adjustments only; content changes go back to Stage 1.

`career-pdf`'s [LaTeX quality reference](productivity/career-pdf/references/latex-quality.md)
is the authoritative CV-PDF verification and delivery gate.

## Adoption

Review this package before copying individual skills into Eric's VPS profile. The local `pdf` package retains the original helpers/tests and revises their routing and operating guidance. Its obsolete CV-production instructions are superseded by `career-pdf`; retain the general utilities. Adoption must include these aligned instructions together, not leave two competing CV-production routes. This local revision is not permission to deploy or install anything.

Eric's existing profile safeguards should remain enabled:

```yaml
auxiliary:
  background_review:
    enabled: false
skills:
  write_approval: true
```
