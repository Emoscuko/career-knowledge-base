---
schema_version: 1
id: project-slime-hunter
kind: project
name: Slime Hunter
project_type: 2D mobile game
role: null
start_date: null
end_date: null
date_status: not_provided
verification_status: source_supported
publication_status: source_reports_published
publication_platforms:
- Apple App Store
- Google Play
links: []
review_refs:
- review-project-links
- review-project-context
- review-publication
source_refs:
- src-cv-slime
- src-ann-slime
claims:
- id: claim-slime-design
  text: Designed a 2D top-down mobile shooter game.
  kind: contribution
  verification_status: source_supported
  source_refs:
  - src-cv-slime
  - src-ann-slime
- id: claim-slime-stack
  text: Used Unity and C# for Slime Hunter.
  kind: technology
  verification_status: source_supported
  source_refs:
  - src-cv-slime
  - src-ann-slime
- id: claim-slime-ai
  text: Implemented state-machine-based enemy AI and a modular architecture.
  kind: contribution
  verification_status: source_supported
  source_refs:
  - src-cv-slime
  - src-ann-slime
- id: claim-slime-rendering
  text: Optimized mobile rendering using object pooling and sprite atlases.
  kind: contribution
  verification_status: source_supported
  source_refs:
  - src-cv-slime
- id: claim-slime-published
  text: Both CVs report publication on the App Store and Google Play; live listings have not been independently
    verified.
  kind: publication
  verification_status: source_supported
  source_refs:
  - src-cv-slime
  - src-ann-slime
---

# Slime Hunter

## Description and problem addressed

A 2D top-down mobile shooter. The sources do not describe a customer problem, business model or target audience beyond mobile game players.

## Technical architecture and features

Unity and C#, state-machine-based enemy AI, modular architecture, object pooling and sprite atlases for mobile rendering optimization.

## Individual contributions

Designed and published the game; developed the reported architecture, enemy behavior and rendering optimizations. Team size and collaborator roles are not supplied.

## Results and publication

The CVs report release on the **App Store and Google Play**. This is a source-supported publication claim, not verification of current availability. Store URLs, release dates, download counts, revenue and performance measurements are absent.

## Associated skills

`skill-csharp`, `skill-unity`, `skill-game-development`, `skill-state-machines`, `skill-modular-architecture`, `skill-object-pooling`, `skill-sprite-atlases`, `skill-mobile-publishing`.

## Evidence and sources

- `src-cv-slime`: general CV, page 1; adds top-down gameplay, object pooling and sprite atlases.
- `src-ann-slime`: annotation CV, page 2.
