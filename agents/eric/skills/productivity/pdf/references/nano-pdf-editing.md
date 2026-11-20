# Optional natural-language PDF editing

Use only for a specifically requested edit to a non-career PDF when an approved,
already available tool can perform it. This is not the route for approved CVs or
letters: edit their Markdown through the owning writing skill, obtain approval
and build a new frozen revision. Never patch a submitted historical PDF.

1. Identify the exact input, requested change, target page and separate output.
   Prefer the editable original and deterministic rebuild when available.
2. Inspect installed `nano-pdf --help` and relevant configuration read-only. Confirm
   page indexing before editing; do not guess and retry with plus/minus one.
3. Establish whether the configured tool sends document content to an external
   model. API-key presence is not permission to share private material. Do not
   install/configure tools, probe credentials or enable external processing as
   part of the edit. If requirements are unmet, stop with the specific limitation.
4. Preserve the original; constrain the requested change. Check text before/after
   across the document for collateral changes, and inspect affected page images
   plus unchanged surrounding layout. File existence/size alone is insufficient.
5. Report exact changes and any unverified fidelity. Do not use a successful
   tool exit as proof of factual correctness, layout preservation or submission.
