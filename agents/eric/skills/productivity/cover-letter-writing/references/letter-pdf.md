# Approved letter PDF procedure

Use only after Rob has approved the saved letter wording and explicitly requested a PDF. This is typesetting, not authority to alter the letter or submit it.

1. Create a new letter revision in the existing application workspace. Copy the approved Markdown verbatim as `letter.md`; keep it separate from CV revisions and do not overwrite an existing PDF.
2. Use locally available tools only. Prefer the established ReportLab letter builder: A4, restrained header, readable 11 pt body, compact contact line and no invented address, recipient or signature. Escape source text before sending it to ReportLab. Do not install software or alter system configuration.
3. Keep the approved body paragraphs exactly and in order. If Rob approves only a replacement sentence, preserve every other character of the latest delivered text and record a small scoped diff.
4. Verify the generated file: it opens; extracted text contains every approved paragraph in order (normalise whitespace only); name, contact details and requested employer/subject are correct; and the PDF has the requested page count. Record the frozen-input hash and a file manifest.
5. Before rendering, check whether a local PDF renderer is available. If none is available, do not retry, install one or claim visual inspection; report that rendered-page inspection is unavailable while distinguishing it from successful text verification.
6. Preserve the editable builder, checks and verification notes with the revision. Deliver the PDF only; local generation is not submission or proof of employer receipt.
