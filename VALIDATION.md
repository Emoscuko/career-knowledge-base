# Validation report

Validated on **2026-11-07**. The evidence is candidate-supplied CV content, not an independent employment or proficiency audit.

## Data and source coverage

- Both supplied PDFs have two pages. All four pages were extracted and visually inspected.
- 17 indexed data/review records; **62 source-traceable claims**; **90 skills** in **15 categories**.
- 68 skills have an explicit source-backed task/background basis; 22 remain listed-only/self-reported. This distinction does not assign numeric proficiency.
- All **26 page/section locators** from the two source documents support at least one claim. Document fingerprints are retained; original files and raw extracts are excluded.
- Syntax, duplicate YAML keys, required identifiers, uniqueness, reference targets, source pages, known date ordering, skill categories/evidence, manifest coverage and local Markdown links: **PASS**.
- Outlier and DataAnnotation.tech remain separate. The unnamed freelance entry is not promoted to a third confirmed employer or assigned to either platform. The 18-item review queue remains open where evidence is incomplete.

## Validator behavior tests

**13 tests passed** using Python 3.9 and PyYAML 6.0.3. The checks cover a valid repository and rejection of duplicate YAML keys, duplicate/missing record IDs, unresolved skill evidence, unsupported skill upgrades, invalid/reversed dates, confirmed placeholders, broken local links, personal email, accidental PDF evidence and remote TeX input.

A missing-ID fixture exposed an error-reporting crash; identifier registration now reports the validation error and skips the malformed record. The regression test prevents recurrence.

Reproduce with:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The local run reused an available PyYAML installation; no global package installation or external validation service was required.

## LaTeX and PDF checks

No installed pdfLaTeX toolchain was available. An official portable **Tectonic 0.17.0** release was downloaded to a temporary directory and checked against the release's published SHA-256 digest. Its standard packages were cached outside the repository. No compiler binary or package bundle is committed.

| Output | Compilation | Pages | Extracted text | Visual inspection |
| --- | --- | --- | --- | --- |
| Reusable template | PASS | 1 | PASS | PASS |
| AI Trainer / Data Annotation Specialist | PASS | 1 | PASS | PASS |
| Backend Software Engineer | PASS | 1 | PASS | PASS |

The final three compiler logs contain no overfull boxes. Pages were rendered with Poppler and inspected for clipping, overlap, typography, section spacing and blank contact-field artifacts. Pypdf and pdfplumber verified selectable text, section order and omission of empty contact separators; Unicode normalization handles standard typographic ligatures. These checks do not guarantee the behavior of every ATS vendor.

Tectonic's input-directory behavior required an explicit repository search path. The shared style now guards pdfTeX-only Unicode mapping commands so XeTeX/Tectonic can use its own mappings. The corrected commands and standalone export instructions are documented in `cv/generation-rules.md`; no shell escape was enabled. Native pdfLaTeX compatibility is designed into the source but was not executed in this environment.

The AI sample prioritizes Outlier audio work, DataAnnotation coding/multilingual assessment and relevant chatbot/content experience. The backend sample prioritizes RevloAI, ASELSAN's actual process-engineering work, SafeRoads, robotics and game architecture. Their evidence maps document selection and gaps. Both omit uncertain employer attribution, unsupported metrics, listed-only production claims and unprovided certifications.

## Privacy and public-source review

- General contact/credential patterns and a local comparison set of five contact/account strings extracted from the private PDFs: **PASS**. Values were not printed by the scan or written into the repository.
- Phone, personal email, home address, personal social profile, original PDFs, full extracts, credentials and private application inputs are excluded.
- Public GitHub identity matched the authenticated connector account. LinkedIn/fitness links could not be fetched and are withheld; no project/store URLs are invented.
- Local contact configuration, output PDFs, rendered previews, caches and compiler logs are ignored. Only sanitized text source is intended for Git.
- The repository uses the account's public GitHub noreply commit identity. Heuristic scanning cannot detect every possible secret or sensitive statement; staged files are also reviewed explicitly.

## GitHub publication

Published: [Emoscuko/career-knowledge-base](https://github.com/Emoscuko/career-knowledge-base). GitHub confirmed visibility `public` and default branch `main`. An unauthenticated API request and archive download independently confirmed public access. All 36 tracked files in the downloaded archive matched initial implementation commit `1fd3eece005d4e002fa46ee571960d308af6d5b8` byte for byte, and the raw README matched the local source. This verification report is added in a follow-up commit; the final delivery also verifies the final published archive. PDFs and private source files were absent from the archive.

For a fresh local copy that has not been published, use the following from its root. Do not recreate or overwrite an existing repository. Configure a public/noreply Git identity first if needed.

```sh
git init -b main
git add .
git diff --cached --check
git commit -m "Build source-traceable career knowledge base and LaTeX workflows"
gh auth login --hostname github.com
gh repo create Emoscuko/career-knowledge-base --public --source=. --remote=origin --push
```

If that name is already taken, choose an available name and update repository URLs in the README and prompts before publishing. If Git is already initialized/committed, skip the first four commands.
