# Contribution intake

Site submissions do not edit the atlas. They create public GitHub issues for review.

## Three feeds checked before a release

1. The curator's running feedback issue.
2. Every site-generated issue carrying the `site-submission` label or the generated submission marker.
3. Standing research and coverage issues.

A release must reconcile all three. A summary of the running thread alone is not a complete feedback pass.

## Automated triage

The `Triage site submissions` workflow recognises the marker added by the public form, applies `site-submission` and `awaiting-curator-review`, and sweeps existing open issues when the workflow is introduced or changed. The labels identify intake; they do not accept the proposed content.

## Editorial states

- `awaiting-curator-review`: received, not yet assessed.
- `needs-source`: a useful question or proposal without adequate public evidence.
- `accepted-for-research`: accepted as a research lead, not yet a public statement.
- `incorporated`: represented in a validated release with an explanatory comment.
- closed as declined, duplicate or out of scope: decision and reason remain public.

## Ivo Velitchkov's viability submission

Issue #21 was successfully created by the website. It was initially missed because the release process read the running feedback thread but did not sweep separate site-generated issues. Release 0.12 fixes the intake process and incorporates the question through independently sourced entries for viability and natural drift. The issue is credited as the prompt, not used as scholarly evidence.
