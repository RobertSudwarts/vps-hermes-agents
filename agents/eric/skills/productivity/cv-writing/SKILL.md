---
name: cv-writing
description: Draft and revise role-specific Markdown CVs and application-form answers for Rob; handle scoped follow-ups and reported submissions. PDF production belongs to career-pdf.
version: 2.0.0
author: Eric
platforms: [linux]
metadata:
  hermes:
    tags: [cv, resume, career, applications, markdown]
    related_skills: [career-pdf, cover-letter-writing, grounded-citations]
---

# CV writing

Build a supported employer-specific reason to interview Rob. Save the editable editorial draft at `/vault/eric/Applications/YYYYMMDD/<application>/working/cv.md`; reuse the existing application workspace.

## Authority and boundaries

- `/vault/eric/workflow-design.md` governs the shared workflow. Read it and relevant `CV/cv_system.md` rules when missing from context or changed; do not reload unchanged authority for routine edits. Surface conflicts to Rob; do not silently retire legacy rules.
- Protected facts live under `/vault/eric/CV/reference/CV/source/`. Never edit them during tailoring. Use relevant sources and confirmed supplements, not generated prose as factual authority. Fresh synthesis is allowed; invented qualifications, titles, dates, responsibilities, scope, outcomes, mechanisms, proficiency or specialist experience are not.
- Preserve direct versus transferable evidence and genuine gaps; personal implementation versus team responsibility, domain familiarity and specialist ownership. Keep confirmations with provenance in existing application evidence, not a competing biography.
- Stage 1 ends with Markdown for Rob's review. Only explicit approval of the exact saved text **and** an explicit PDF request permit handoff to `career-pdf`, which must freeze that text without rewriting it. Internal review or a one-shot drafting request is not approval.
- No external submission, outreach, uploads, software/configuration changes, automatic skill mutation or self-improvement. Discovery belongs to `job-discovery`; letters to `cover-letter-writing`; needed employer verification to `grounded-citations`.

## Load only the relevant route

- New role, focused open application or substantive rewrite: [drafting method](references/substantive-cv.md), then [editorial review](references/review-checklist.md).
- Sentence/skills edit, local review or PDF handoff: [follow-ups](references/follow-ups.md).
- Form answers, including a single-answer retry: [form answers](references/application-form-answers.md).
- Rob reports submission or asks about application records: [application records](references/application-records.md).
- Separately requested workspace maintenance only: [housekeeping](references/workspace-housekeeping.md). Never load or execute this as routine drafting cleanup.

Reuse loaded evidence; retrieve only missing or changed facts. Show the requested draft or changed passage with material uncertainties outside employer-facing text. Keep bulk records on disk and return concise check results; fewer reads alone do not prove token or billing savings.
