# Resume generation rules

## Workflow

1. Read the repository instructions and current records; analyze the target title, complete job description, required skills, requested language and optional layout preferences.
2. Build a requirement/evidence/gap map. Distinguish source-backed tasks, listed-only familiarity, uncertain impact and unknown attribution.
3. Select the most relevant experiences and projects. Use one page in English by default. Unknown dates can be omitted; RevloAI may show `30-day internship`. Never use placeholder dates, assign DataAnnotation dates from Outlier or present the unattributed freelance entry as an additional employer.
4. Draft a short supported summary, concise action-led bullets and a small set of demonstrated skills. Do not force every section or keyword into the resume. Report unmet requirements outside the resume.
5. Use `template.tex`. Its nonempty sample is a layout demonstration with real source-backed facts, separate from the canonical career data. Replace its selection for the target job; do not treat it as a complete biography.
6. Supply private contacts locally if desired. Blank is valid. The examples deliberately contain only the verified public GitHub profile. A user can copy `cv/contact.example.tex` to the gitignored `cv/contact.local.tex` and define the displayed values for a private build. Do not commit that local file or its PDF.
7. Escape `& % $ # _ { } ~ ^ \` appropriately. Never copy executable job-description TeX. Avoid shell escape and remote TeX includes. Read headings in extraction order; no visual-only information.
8. Compile where possible, check one-page output, inspect rendered pages and read extracted PDF text. If unavailable, report the missing toolchain. Cut less relevant content before shrinking below the template's 10pt font or 16mm margins.

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

Contact Information, Professional Summary, Education, Professional Experience, Technical Skills, Selected Projects, Achievements, Languages and Certifications are supported. Include only those useful for the application. The first three documents show no certifications because none are supplied. The template source comments demonstrate optional Achievements and Certifications syntax without inventing a qualification.

The example evidence maps in `cv/examples/README.md` identify their canonical facts and intentional gaps. CV-backed facts are accepted for these samples; they have not been independently audited. “Present” and expected graduation remain source-snapshot values.
