# Examples with complete experience coverage

These are illustrative role-based selections dated **2026-11-07**, not applications to actual job postings. Claims are backed by the supplied CVs; employment, proficiency and publication have not been independently audited. Career facts live in the canonical records; `cv/generation-policy.yaml` controls coverage. Both samples include all five supported distinct experiences. Relevance changes order and detail, while projects and skills remain selected.

| Scenario | LaTeX | Emphasis |
| --- | --- | --- |
| AI Trainer / Data Annotation Specialist | [ai-trainer.tex](ai-trainer.tex) | Outlier audio guidelines; DataAnnotation coding, multilingual and response comparison; RevloAI LLM context; concise ASELSAN and content creation |
| Backend Software Engineer | [backend-engineer.tex](backend-engineer.tex) | RevloAI Go, Spring Boot, Azure and software practices; ASELSAN workflow analysis; SafeRoads and game architecture; concise Outlier, DataAnnotation and content creation |

## Experience inventory

| Record | AI trainer | Backend engineer |
| --- | --- | --- |
| `experience-outlier` | Detailed primary experience | Concise additional experience |
| `experience-dataannotation` | Detailed primary experience | Concise additional experience |
| `experience-revloai` | Supporting additional experience | Detailed primary experience |
| `experience-aselsan` | Concise additional experience | Primary engineering experience |
| `experience-content-creation` | Concise additional experience | Concise additional experience |
| `experience-freelance-unattributed` | Deferred: may duplicate the named platforms | Deferred: may duplicate the named platforms |

Deferral preserves the attribution restriction; it does not omit a separately established job. Known but less relevant roles remain visible. Unknown dates remain blank or show a supported duration. No owner-requested exclusions apply to these examples.

## AI example evidence

| Resume claim group | Canonical record | Claim IDs |
| --- | --- | --- |
| Summary, code/multilingual assessment, comparison | [DataAnnotation.tech](../../experience/dataannotation.md) | `claim-dataannotation-code`, `claim-dataannotation-multilingual`, `claim-dataannotation-comparison`, `claim-dataannotation-reasoning` |
| Audio annotation and guidelines, role/start date | [Outlier](../../experience/outlier.md) | `claim-outlier-role`, `claim-outlier-audio`, `claim-outlier-guidelines` |
| Go backend and chatbot integration | [RevloAI](../../experience/revloai.md) | `claim-revloai-role`, `claim-revloai-go`, `claim-revloai-llm` |
| Concise engineering internship | [ASELSAN](../../experience/aselsan.md) | `claim-aselsan-role`, `claim-aselsan-workflows` |
| Independent content and editing | [Content creation](../../background/content-creation.md) | `claim-content-original`, `claim-content-editing` |
| Education and languages | [Education](../../background/education.md), [Languages](../../background/languages.md) | `claim-education-degree`, `claim-education-graduation`, `claim-education-gpa`, `claim-language-turkish`, `claim-language-english`, `claim-language-german` |

No employer is assigned the unattributed Java, prompt or test-case claims. DataAnnotation.tech is undated; its dates are not copied from Outlier. No evaluation language pair is asserted. Content creation is undated. “Present” is only the supplied source snapshot.

## Backend example evidence

| Resume claim group | Canonical record | Claim IDs |
| --- | --- | --- |
| Go services, Azure, chatbot, OOP/design, Scrum/reviews | [RevloAI](../../experience/revloai.md) | `claim-revloai-role`, `claim-revloai-go`, `claim-revloai-llm`, `claim-revloai-azure`, `claim-revloai-design`, `claim-revloai-scrum` |
| Engineering role, workflow and optimization | [ASELSAN](../../experience/aselsan.md) | `claim-aselsan-role`, `claim-aselsan-workflows`, `claim-aselsan-optimization` |
| CI/CD pipeline | [SafeRoads](../../projects/saferoads.md) | `claim-saferoads-pipeline` |
| Game design, AI, rendering and publication | [Slime Hunter](../../projects/slime-hunter.md) | `claim-slime-design`, `claim-slime-stack`, `claim-slime-ai`, `claim-slime-rendering`, `claim-slime-published` |
| Concise audio role | [Outlier](../../experience/outlier.md) | `claim-outlier-role`, `claim-outlier-audio`, `claim-outlier-guidelines` |
| Concise coding/multilingual role | [DataAnnotation.tech](../../experience/dataannotation.md) | `claim-dataannotation-role`, `claim-dataannotation-code`, `claim-dataannotation-multilingual`, `claim-dataannotation-comparison` |
| Concise independent content work | [Content creation](../../background/content-creation.md) | `claim-content-original` |
| Education and languages | [Education](../../background/education.md), [Languages](../../background/languages.md) | All three education claims and all three language claims listed above |

The title expresses the target field, while the actual internships keep their source titles. RevloAI shows a 30-day duration rather than invented dates. Publication is CV-reported; current listings are not verified. ASELSAN is process engineering, not a software engineering internship.

## Intentional gaps and shared rules

- Neither sample claims measured impact, expertise, years of professional experience or leadership.
- Database, Docker, GitHub Actions, REST, microservices, JWT and RLHF declarations remain in the knowledge base but are omitted from these demonstrated-evidence selections.
- No certification, specific award event or project link is fabricated.
- Private contacts are blank by default. Only the verified GitHub profile is shown.
- Both target one page while preserving all five supported roles. Optional project content is reduced before any experience; use a second page when needed. Run `python3 scripts/validate_resume.py cv/examples/ai-trainer.tex` (and the backend file) for the inventory report. The repository validator also checks the template and both examples automatically. Compile from the repository root using [the build instructions](../generation-rules.md), then check rendered layout and extracted text. See [VALIDATION.md](../../VALIDATION.md) for the checks actually run in this environment.
