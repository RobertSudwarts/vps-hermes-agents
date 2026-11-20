---
name: career-pdf
description: Build a frozen PDF revision from an explicitly approved role-specific Markdown CV. Never use for drafting or revising CV content.
version: 1.0.0
author: Eric
platforms: [linux]
metadata:
  hermes:
    tags: [cv, pdf, latex, applications, production]
    related_skills: [cv-writing, pdf]
---

# Career PDF production

Use this skill only when Rob explicitly asks to build or compile a PDF from an approved `working/cv.md`.

## Stage 2: production, not drafting

1. Identify the exact application and approved Markdown input.
2. Create the next `revisions/rNNN/` directory without overwriting an existing revision.
3. Copy the exact Markdown input into that revision before building and verify its hash against the approved file. Validate its supported structure read-only; incompatibility returns to review, never silent repair. Pass this frozen copy, not the mutable working file, to the builder.
4. Use the explicitly approved frozen ModernCV release under `/vault/eric/templates/moderncv/` (currently v003; v004 is a candidate, not an automatic upgrade). Read that release’s build contract; preserve releases and existing artifacts.
5. Follow `references/latex-quality.md`.
6. Retain a SHA-256 manifest for the frozen input and generated revision artifacts. Report artifact paths, page count, completed checks, warnings and any verification limitation.

Do not reread the role to change the hiring argument, alter `working/cv.md`, modify protected career sources, change the shared template, or create a submission record.

If a build needs wording or factual changes, stop and return the issue to `cv-writing` for Markdown revision and renewed approval. If it needs typography, margin or shared-template changes, stop and report a separately scoped production/template issue to Rob. Do not alter the approved Markdown or shared template. A build may use only narrowly scoped, recorded, revision-local layout corrections that preserve the frozen text, approved typography, margins and template release.
