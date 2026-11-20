# Eric's focused career skills

This is a proposed replacement for Eric's career workflow layer. It is deliberately separate from the generic Hermes skills currently installed on the VPS.

## Scope

The set contains five skills:

- `job-discovery` — find, assess and track opportunities.
- `grounded-citations` — verify external claims and retain evidence.
- `cv-writing` — prepare a tailored Markdown CV for review.
- `cover-letter-writing` — prepare a separate, role-specific letter.
- `career-pdf` — turn an explicitly approved Markdown CV into a frozen PDF revision.

The protected career record remains under `/vault/eric/CV/`; these skills must never modify it while tailoring. `/vault/eric/workflow-design.md` is the shared durable workflow policy.

## CV hand-off

`cv-writing` is Stage 1: it creates or revises `working/cv.md`. It does not build a PDF.

`career-pdf` is Stage 2: it runs only when Rob explicitly asks to build the approved Markdown. It copies that exact file into `revisions/rNNN/` before compiling. It may make recorded, revision-local layout adjustments only; content changes go back to Stage 1.

## Adoption

Review this package before copying individual skills into Eric's VPS profile. Do not replace the existing generic `pdf` skill. The new `career-pdf` skill is intentionally separate.

Eric's existing profile safeguards should remain enabled:

```yaml
auxiliary:
  background_review:
    enabled: false
skills:
  write_approval: true
```

