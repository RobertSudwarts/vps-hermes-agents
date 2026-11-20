---
name: career-pdf
description: Build a frozen PDF revision from an explicitly approved role-specific Markdown CV. Never use for drafting or revising CV content.
version: 1.0.0
author: Eric
platforms: [linux]
metadata:
  hermes:
    tags: [cv, pdf, latex, applications, production]
    related_skills: [cv-writing]
---

# Career PDF production

Use this skill only when Rob explicitly asks to build or compile a PDF from an approved `working/cv.md`.

## Stage 2: production, not drafting

1. Identify the exact application and approved Markdown input.
2. Create the next `revisions/rNNN/` directory without overwriting an existing revision.
3. Copy the exact Markdown input into that revision before building. This frozen copy is the source of truth for the PDF.
4. Use the approved ModernCV template and shared builder under `/vault/eric/templates/moderncv/`.
5. Follow `references/latex-quality.md`.
6. Report artifact paths, page count, completed checks, warnings and any verification limitation.

Do not reread the role to change the hiring argument, alter `working/cv.md`, modify protected career sources, change the shared template, or create a submission record.

If a build needs wording, factual, typography, margin or template changes, stop and return the issue to `cv-writing`. A build may use only narrowly scoped, recorded, revision-local layout corrections.

