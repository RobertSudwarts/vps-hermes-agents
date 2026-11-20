# General LaTeX production

For non-career LaTeX documents only. Approved CVs use `career-pdf`; its reference
owns the career presentation, frozen input, revision and manifest rules. Do not
load CV methodology or canonical career history for generic compilation.

Use an existing approved project source/template and installed compiler. Preserve
reviewed wording, layout choices and existing outputs. Compile with shell escape
disabled and fail on errors, for example `pdflatex -no-shell-escape
-interaction=nonstopmode -halt-on-error`; use the project's documented build command
and repeat only when cross-references/build requirements call for it.

Inspect the final compiler log for errors, missing glyphs and unresolved layout
warnings. Diagnose the cause before another attempt; do not suppress warnings with
blanket settings such as `\sloppy` or rewrite content to make a check pass.
Keep source, build options/log and final output sufficient for reproduction.

Check the actual final PDF's page count, text completeness, literal names/dates
and visible layout using [verification](verification.md). Extraction success is
not visual success. Do not silently change fonts, margins or approved text.
Request separately scoped content/presentation changes when necessary and report
unavailable checks honestly. No dependency installation or external compilation
service is implicit in a build request.
