---
schema_version: 1
id: background-languages
kind: languages
verification_status: source_supported
languages:
- name: Turkish
  level: Native
  claim_ref: claim-language-turkish
- name: English
  level: C1
  description: Advanced
  claim_ref: claim-language-english
- name: German
  level: A2
  description: Elementary
  claim_ref: claim-language-german
review_refs:
- review-task-languages
source_refs:
- src-cv-languages
- src-ann-languages
claims:
- id: claim-language-turkish
  text: 'Turkish: Native.'
  kind: language
  verification_status: source_supported
  source_refs:
  - src-cv-languages
  - src-ann-languages
- id: claim-language-english
  text: 'English: C1 (Advanced), reported in both CVs; no test or certificate supplied.'
  kind: language
  verification_status: source_supported
  source_refs:
  - src-cv-languages
  - src-ann-languages
- id: claim-language-german
  text: 'German: A2 (Elementary), reported in both CVs; no test or certificate supplied.'
  kind: language
  verification_status: source_supported
  source_refs:
  - src-cv-languages
  - src-ann-languages
---

# Languages

- Turkish: Native.
- English: C1 (Advanced).
- German: A2 (Elementary).

These are candidate-reported language levels, supported by the CVs rather than a supplied examination certificate. Do not invent a TOEFL/IELTS score, certification or language pair for the multilingual evaluation work.

## Evidence and sources

- `src-cv-languages`: general CV, page 2.
- `src-ann-languages`: annotation CV, page 2.
