# Data contract (schema version 1)

Ordinary YAML and Markdown are the storage format. `scripts/validate.py` enforces this contract with PyYAML; no database, service or generator is required to read the data. YAML duplicate keys are rejected. Quote date strings and skill names such as `C#` when hand-editing if needed.

## Stable identifiers and discovery

`index.yaml` maps record IDs to canonical paths. IDs use lowercase kebab case and are globally unique across records, skills, claims, sources, locators and review items. Do not change IDs when editing prose or renaming a file; update the manifest path instead. Examples: `experience-revloai`, `project-saferoads`, `skill-go`, `claim-revloai-go`, `src-cv-revloai`.

Each data document/front matter has `schema_version: 1` and `id`. Career records also have `kind`, `verification_status`, `source_refs` and `claims`. Empty arrays or `null` are intentional unknown/not-supplied values. Do not add empty records for hypothetical projects.

## Evidence model

`sources.yaml` contains:

- `documents`: source ID, original document label, SHA-256 fingerprint, page count, received date, visibility and evidence scope. Private files are not committed. Later owner confirmations can use a descriptive document label and a fingerprint of a retained private note, or a public verified source with its retrieval details; keep the same traceable structure and do not invent a PDF page.
- `locators`: ID, `source_id`, `pages` and section name. Pages must fall within the document's page count. For a non-paginated owner confirmation, use `page_count: 0` and `pages: []` with a descriptive section. Add source type/retrieval metadata as needed.

Each claim has `id`, `text`, `kind`, `verification_status` and nonempty `source_refs` pointing to locators. Claim kinds distinguish role, responsibility, contribution, technology, publication, impact, education, language, achievement, self-report and skill declaration. Record-level support does not override a claim's uncertainty or attribution restrictions.

| Status | Meaning | Generation policy |
| --- | --- | --- |
| `source_supported` | Explicit statement/task in a supplied source | Usable with exact scope and review restrictions; not independently audited |
| `externally_verified` | Narrow external check with method/date | Only the stated fact is externally checked |
| `self_reported` | Listed skill/profile familiarity without task demonstration | Preserve; prefer stronger evidence; never imply production usage |
| `needs_confirmation` | Uncertain impact, attribution or conflicting detail | Follow review policy; do not turn into a confirmed assertion |
| `not_provided` | Evidence absent | Omit or report missing; never infer none exists |

## Record fields

Experiences: organization (nullable), role, location (nullable), `start_date`/`end_date` (nullable `YYYY-MM`), `ongoing_as_of_source` (true/false/null), `date_status`, sources, claims, optional source snapshot, duration and review references. A known duration is not a calendar date. Only `ongoing_as_of_source: true` with a `source_as_of` permits “Present” in that snapshot. Unknown end dates alone do not imply current employment.

Projects: name, project type, role (nullable), dates (nullable), date status, publication status, verified links (or empty list), sources, claims and review references. Markdown sections preserve architecture, individual contributions, results, features, limitations and associated skill IDs. Do not invent a problem statement absent from the sources.

Education: institution, degree, field, instruction language, expected graduation, GPA value/scale and supporting claims. Enrollment and expected dates differ from degree completion.

Languages and achievements use discrete claims. `background/certifications.md` explicitly records missing evidence with `not_provided`; it does not assert no certifications exist.

## Skills

`skills.yaml` defines a unique category registry and a flat `skills` array. Each skill has `id`, `name`, `category` (category ID), `tags`, `related_experiences`, `related_projects`, `related_background`, nonempty `evidence_refs` (claim IDs), `verification_status` and `evidence_type`. Optional `notes` preserve scope. A supported skill must cite at least one supported task/background claim; list-only evidence cannot establish it. Only language skills currently have source-backed `proficiency` metadata.

Related record references require the right record kind. Do not add an experience/project association merely because its framework is compatible with the skill. Tags are search terms, not additional qualifications. New categories are allowed; validation does not hardcode a particular skills list.

## Review items

`DATA_REVIEW.md` front matter contains `review_items`: ID, open/resolved status, category, affected `record_refs`, question and generation policy. Record `review_refs` must resolve. A resolved item also needs a resolution and nonempty `source_refs`. An unresolved item can coexist with usable supported facts.

## Validation boundaries

The validator checks syntax, uniqueness, required fields, references, evidence status, month/date ordering, known source pages, manifest coverage, local Markdown links, safe LaTeX inputs and likely private contacts/secrets. It cannot prove employment, detect every semantic exaggeration, establish live store availability or guarantee an ATS vendor's parsing. Source review, rendered PDF inspection and private-data review remain necessary. Optional external URL checks report access failures separately from local data errors.


## Persistent resume preferences and coverage

`cv/generation-policy.yaml` is the canonical candidate preference, separate from career facts and layout. It is a versioned data record included in the manifest. It requires all source-supported/externally-verified distinct experiences, permits relevance-based ordering/detail, keeps other roles concise and gives coverage priority over the preferred one-page limit. Only explicit owner-requested exclusions or attribution-uncertain records can leave the experience section. Optional project/skill selection is unchanged.

`profile.yaml` -> `experience_refs` must cover every indexed `kind: experience` record exactly once, including `background/content-creation.md`. Required coverage is computed from these current records and the policy's eligible statuses; it is not a hardcoded employer list. A newly added supported experience automatically becomes required.

LaTeX work entries use `\ResumeExperience{record-id}{organization}{role}{dates}{location}`; the style delegates the four displayed fields to `\ResumeEntry` and never prints the stable ID. Education still uses `\ResumeEntry`. The pure coverage checker validates body entries and organization association, rejects missing/duplicate/unknown/uncertain work entries, and returns included/deferred/excluded decisions. It is not a full TeX interpreter or a substitute for source review and rendered PDF inspection. Literal organization/role fields are required; dates/location may remain empty.

`scripts/validate.py` checks the repository template/examples by default. `scripts/validate_resume.py <file.tex>` applies the same rules to a new generated document and prints the inventory report. An explicit owner-requested exclusion is recorded through `--exclude ID=OWNER_REQUEST_REASON` and must be disclosed outside the resume; this escape hatch cannot establish whether the user actually authorized it. AI instructions require that authorization rather than assuming it.
