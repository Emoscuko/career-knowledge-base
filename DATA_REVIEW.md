---
schema_version: 1
id: data-review
as_of: '2026-11-07'
review_items:
- id: review-freelance-attribution
  status: open
  category: attribution
  record_refs:
  - experience-freelance-unattributed
  - experience-outlier
  - experience-dataannotation
  question: Does the general CV Freelance entry summarize Outlier, DataAnnotation.tech, both or another contract?
    Which platform involved Java evaluation, prompts and test cases?
  generation_policy: Keep its task facts, but omit the unattributed experience from default resumes and never
    count it as an additional employer.
- id: review-dataannotation-dates
  status: open
  category: dates
  record_refs:
  - experience-dataannotation
  question: What are the start/end dates and current status of DataAnnotation.tech?
  generation_policy: Use an undated entry when relevant; never borrow Outlier dates.
- id: review-revloai-dates
  status: open
  category: dates
  record_refs:
  - experience-revloai
  question: What are the calendar start/end dates or at least year of the 30-day RevloAI internship?
  generation_policy: Use 30-day internship without fabricated calendar dates.
- id: review-currentness
  status: open
  category: currentness
  record_refs:
  - profile-emirhan-atar
  - experience-outlier
  - experience-freelance-unattributed
  - background-education
  question: Are ongoing roles, student status, GPA and expected June 2027 graduation still current?
  generation_policy: Present means the 2026-11-07 source snapshot; reconfirm for later applications.
- id: review-project-links
  status: open
  category: links
  record_refs:
  - project-robotic-positioning
  - project-slime-hunter
  - project-saferoads
  question: Provide public repositories, demos and Slime Hunter App Store / Google Play listing URLs.
  generation_policy: No project URL is invented or inferred from names.
- id: review-project-context
  status: open
  category: context
  record_refs:
  - project-robotic-positioning
  - project-slime-hunter
  - project-saferoads
  question: What are the project dates, academic/personal/commercial context, team sizes and individual boundaries?
    Which languages/libraries supported robotics and SafeRoads?
  generation_policy: Describe only the supplied components and contributions; omit unknown context.
- id: review-publication
  status: open
  category: publication
  record_refs:
  - project-slime-hunter
  question: Confirm current store availability, exact listings and release dates for Slime Hunter.
  generation_policy: May say the CVs report publication; no claim about current availability, downloads or
    revenue.
- id: review-saferoads-impact
  status: open
  category: impact
  record_refs:
  - project-saferoads
  question: Can the reported reduction in manual deployment errors be substantiated with a baseline and result?
  generation_policy: Use the documented pipeline contribution; omit significantly and any invented metric.
- id: review-performance
  status: open
  category: impact
  record_refs:
  - experience-revloai
  question: Is there evidence behind high-performance Go services, measured load, latency or improvement?
  generation_policy: Use developed Go backend services; omit performance adjectives and invented scale.
- id: review-task-languages
  status: open
  category: scope
  record_refs:
  - experience-dataannotation
  - background-languages
  question: Which languages were used for multilingual AI evaluation? Are C1/A2 self-assessments or backed
    by tests?
  generation_policy: Keep Turkish Native, English C1 and German A2 as CV-reported levels; do not infer evaluation
    language pairs or certifications.
- id: review-audio-details
  status: open
  category: scope
  record_refs:
  - experience-outlier
  question: Which audio annotation task types, tools and languages can be disclosed?
  generation_policy: Do not add transcription, diarization, timestamping, task volumes or tool names.
- id: review-education
  status: open
  category: dates
  record_refs:
  - background-education
  question: What is the enrollment start date and when was the 3.72/4.00 GPA recorded?
  generation_policy: Keep expected graduation and GPA as source facts; do not claim a completed degree or honors.
- id: review-awards
  status: open
  category: achievements
  record_refs:
  - background-achievements
  question: What were the hackathon and game jam names, dates, organizers, team/project details and public
    evidence?
  generation_policy: Keep the reported 3rd and 2nd places generic; omit from examples until context is clearer.
- id: review-athletic-training
  status: open
  category: currentness
  record_refs:
  - background-achievements
  question: As of what date did seven years of training apply, and is this useful for a target application?
  generation_policy: Retain the source duration; do not increment it or imply coaching credentials.
- id: review-content-dates
  status: open
  category: dates
  record_refs:
  - experience-content-creation
  question: When did independent content creation start, and are audience metrics or portfolio examples available?
  generation_policy: Keep the work undated; no followers, engagement rate, revenue or editing-tool claims.
- id: review-social-links
  status: open
  category: privacy_and_links
  record_refs:
  - experience-content-creation
  - profile-emirhan-atar
  question: Confirm the public professional LinkedIn target and whether a verified fitness account should be
    included.
  generation_policy: GitHub identity is verified against the authenticated connector. LinkedIn and fitness
    URLs could not be fetched. Their targets and account identifiers are withheld; the personal social profile
    stays excluded.
- id: review-listed-skills
  status: open
  category: evidence
  record_refs:
  - skills-inventory
  question: Can task evidence be added for Python, TypeScript, SQL, C++, REST APIs, microservices, JWT, Azure
    Blob Storage, GitHub Actions, Docker, PostgreSQL, MongoDB, data modeling, RLHF, UML and Git?
  generation_policy: Preserve listed-only skills as self_reported; do not upgrade them to demonstrated production
    expertise.
- id: review-certifications
  status: open
  category: missing
  record_refs:
  - background-certifications
  question: Are there certifications to add with issuer, dates and verification links?
  generation_policy: Omit Certifications until evidence is supplied; not provided does not mean none exist.
---

# Data review

Both CVs were read completely and all four pages were visually checked. No direct conflict was found in the name, education, GPA, expected graduation, ASELSAN dates, language levels or placements.

## Differences reconciled

- **Outlier AI and DataAnnotation.tech stay distinct.** The annotation CV names audio work at Outlier and coding/multilingual work at DataAnnotation.tech. The general CV instead has one unnamed freelance Java-evaluation entry. Shared dates do not establish a shared employer.
- **Unique technical details are retained.** The general CV adds RevloAI Azure infrastructure/deployment work, OOP, design patterns, daily Scrum and code reviews; robotics homography; Slime Hunter top-down gameplay, object pooling and sprite atlases; and broader technical skill declarations.
- **Unique annotation and media work is retained.** The annotation CV adds audio guidelines, structured response comparison, multilingual quality assessment and independent fitness/entertainment content creation.
- **SafeRoads role labels differ in specificity.** “DevOps & Infrastructure Developer” and “DevOps Developer” are retained as variants, with no evidence of two roles.
- **Qualitative impact remains uncertain.** The general CV calls Go services high-performance and says the SafeRoads pipeline significantly reduced errors. Neither source supplies a measurement; examples omit these adjectives.
- **Private information is excluded.** Original PDFs, raw extracts, phone, email and personal social identifiers are not part of this repository. Public GitHub identity was matched against the authenticated account; other profile links await live verification.

## Confirmation queue

The YAML front matter contains the complete, machine-readable queue, including each question, affected records and the rule to follow while it remains unresolved. The highest priorities are freelance attribution, missing internship/platform dates, and project/store links. No missing detail blocks use of the supported facts.

When resolving an item, add owner-supplied evidence to `sources.yaml`, update the affected claims/fields and skills, and mark the item `resolved` with a resolution and source reference. Never overwrite contradictory history without a note.
