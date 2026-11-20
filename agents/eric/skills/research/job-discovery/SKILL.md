---
name: job-discovery
description: Find, revisit and assess career opportunities for Rob while preserving a compact, evidence-backed opportunity register.
version: 2.0.0
author: Eric
platforms: [linux]
metadata:
  hermes:
    tags: [jobs, vacancies, career, research, monitoring]
    related_skills: [grounded-citations, cv-writing]
---

# Job discovery

Use this skill to find opportunities, refresh a known pipeline, or assess a named role. It owns discovery and fit assessment; it does not draft CVs, cover letters, applications or outreach.

## Sources of truth

- `/vault/eric/Research/job-search/README.md` defines the active search brief.
- `sources.json` is the source watchlist and `opportunities.json` is the working register.
- `/vault/eric/CV/` is the protected factual career record. Do not create a competing biography or modify it during discovery.

Rob chooses whether to pursue an opportunity. A recommendation is an assessment, not a veto or an application decision.

## Choose the smallest route

- **Pipeline snapshot:** read the saved register and report its recorded state. Do not turn it into a fresh scan.
- **Incremental scan:** refresh selected validated sources mechanically, inspect changes, then review only new or materially changed candidates.
- **Bounded role pass:** use `references/bounded-assessment.md`; declare a shared review cap before delegating work.
- **New source or parser:** use `references/source-onboarding.md`; do not install software or change a source contract without permission.

## Assessment rules

Screen cheaply before deeper work: role status, location, workplace language, seniority and role-defining work. Verify a promising recommendation against the primary advert and actual career evidence.

Exclude roles where professional German is explicitly mandatory. Flag German when it is preferred or unclear. Do not infer eligibility, language, salary, seniority or technical proficiency from silence.

Keep decisions precise: `shortlisted` for a positive research judgement, `reviewed` for a conditional lead, and `excluded` only with a recorded concrete reason. Preserve prior decisions and application links.

## Cost discipline

Keep feeds, source bodies and register history in files. Use deterministic collection, deduplication and diffing before model review. Give each delegated worker a compact, bounded candidate packet; do not hand it the full register, all source transcripts or an open-ended search brief.

Return a concise shortlist with exact primary links, fit, reservation, observation date and any completeness warning.

