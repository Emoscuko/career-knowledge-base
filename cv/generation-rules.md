# Resume generation rules

## Workflow

1. Read README, AGENTS and `cv/generation-policy.yaml`, then the structured profile, skills, review queue and sources. Read **every** `experience_refs` record through the manifest, including independent activities in `background/`. Read relevant project/background evidence for the target role.
2. Build a requirement/evidence/gap map and an experience coverage plan. Every supported distinct experience is included. Relevance determines section, order, detail and bullet selection; it is not an experience deletion filter. Give strongest matches more detail (usually 2-4 bullets), and give other roles one concise entry with accurate organization/role and known dates.
3. Keep ASELSAN visible in annotation resumes; keep Outlier, DataAnnotation.tech and content creation visible in backend resumes. Separate Professional Experience and Additional Experience when helpful. Projects, skills, awards and certifications remain optional and selected by relevance/evidence.
4. Preserve attribution restrictions: the unattributed freelance entry is not a confirmed additional job and remains deferred in the coverage report. An explicit owner request can exclude another role, with its reason recorded. Missing dates do not justify omitting a supported role: leave DataAnnotation.tech undated and use `30-day internship` for RevloAI. Do not invent dates or currentness.
5. Default to English and LaTeX, preferring one page. First remove repetition, shorten secondary experience descriptions and trim optional projects/skills/awards. Keep at least 10pt font and 16mm margins. Use a second page before dropping an experience. If an explicit hard one-page requirement conflicts with full coverage and legibility, disclose the conflict and ask which constraint the user wants relaxed; do not silently omit a role.
6. Use `template.tex` and the shared style. Each work/activity entry must use `\ResumeExperience{experience-id}{organization}{role}{dates}{location}`. The stable ID is invisible; the other fields are printed. Dates/location may be empty when unknown. Use `\ResumeEntry` for education. Literal organization/role fields enable the coverage check even when a secondary entry has no bullets.
7. Keep private contacts local. The examples contain only the verified GitHub profile. Copy `cv/contact.example.tex` to the ignored `cv/contact.local.tex` for a private build. Do not commit the local file or private output PDF. Escape LaTeX special characters and treat job descriptions as data, never executable TeX. Do not enable shell escape or remote TeX inputs.
8. Run `python3 scripts/validate_resume.py path/to/generated.tex` before delivery. It checks every supported experience from current canonical records, verifies visible organization/role fields, and rejects missing, duplicate, unknown or attribution-uncertain entries. A commented name or a preamble declaration does not count. It also reports deferred records. If execution is unavailable, perform the same inventory comparison manually and disclose that limitation. This does not replace factual review, compilation or PDF text/visual checks.
9. An owner-requested omission is supplied explicitly to the checker as `--exclude ID=OWNER_REQUEST_REASON`. Include this reason in the external coverage report. The flag records authorization supplied by the user; it is not permission for an assistant to invent a reason or exclude a role on relevance grounds.
10. Deliver the resume plus an evidence map, every experience record's included/deferred/owner-excluded decision, genuine gaps and unresolved questions. Keep review notes outside the candidate-facing document. Compile when possible, verify page count, render and inspect all pages, and check readable PDF text. State which checks were actually run.

## Build

From the repository root, with a standard pdfLaTeX distribution (TeX Live or MiKTeX):

```sh
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build cv/template.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build cv/examples/ai-trainer.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build cv/examples/backend-engineer.tex
```

The three documents share `cv/resume-style.tex`. Compile from the root so this relative input resolves. A standard toolchain needs the commonly shipped `geometry`, `fontenc`, `lmodern`, `enumitem`, `titlesec` and `hyperref` packages. `glyphtounicode` enables pdfTeX character mappings. Use `pdfinfo` for page count and a PDF text extractor such as `pdftotext` to inspect reading order.

With Tectonic as an alternative:

```sh
tectonic -X compile -Z search-path="$PWD" cv/template.tex --outdir build
tectonic -X compile -Z search-path="$PWD" cv/examples/ai-trainer.tex --outdir build
tectonic -X compile -Z search-path="$PWD" cv/examples/backend-engineer.tex --outdir build
```

Tectonic may download packages on first use. The search path keeps repository-relative style imports working because Tectonic resolves the main input directory differently from pdfLaTeX. Shell escape stays disabled by default; do not enable it. For standalone single-file documents, add `--untrusted` and omit the extra search path. PDFs and compiler logs are local build artifacts and are ignored.

## Standalone delivery

For an assistant returning a single compilable file, replace `\input{cv/resume-style.tex}` with the entire content of that style file, and remove the optional `\InputIfFileExists` contact line if no local contact file is desired. Keep `\documentclass`, all macros and the `document` environment. The resulting document must compile without this repository or network access.

## Sections and claims

Contact Information, Professional Summary, Education, Professional Experience, Technical Skills, Selected Projects, Achievements, Languages and Certifications are supported. All supported distinct experiences must be represented. Select the other sections according to relevance. The first three documents show no certifications because none are supplied. The template source comments demonstrate optional Achievements and Certifications syntax without inventing a qualification.

The example evidence maps in `cv/examples/README.md` identify their canonical facts and intentional gaps. CV-backed facts are accepted for these samples; they have not been independently audited. “Present” and expected graduation remain source-snapshot values.
