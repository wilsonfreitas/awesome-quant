---
name: bprr
description: Use when the user asks to review all open awesome-quant PRs, review unreviewed PRs, bulk review, or mentions "bprr".
---

# BPRR: Bulk PR Reviewer

Prepare a selective decision batch for README contributions, corrections and cleanup under
[CONTRIBUTING.md](../../../CONTRIBUTING.md#review-capacity-and-outcomes).

**REQUIRED SUB-SKILL:** Use `sprr` as the canonical policy for reviewing each pull request. Read
it before starting the bulk review and apply its hard rules, workflow evidence rules, validation
checklist, verdicts, output fields, and action/freshness contract.

## Hard Rules

1. Use GitHub MCP tools for PR operations. Do not use `gh` for PR review, comments, labels,
   closing, or merging. If tools are unavailable, report the blocker and point to `docs/codex-setup.md`.
2. The `reviewed` label is never the sole skip reason. Select new, changed or stale submissions
   since the last attributable review, including body-only changes. Unknown prior evidence is
   unknown, not passed. Retain labels; no mass re-review/rejection of already-open PRs.
3. Apply `sprr` independently to every PR selected for detailed review. Shared retrieval saves
   work, but findings, eligibility and readiness remain specific to each PR/entry.
4. Present findings and exact actions before writes. One explicit bundle selection is sufficient
   for the unchanged listed scope, subject to `sprr`'s freshness checks; no repeat identical consent.
5. Classification labels cannot imply approval. No automatic PR writes.

## Bulk Workflow

1. Establish remaining human PR review minutes from the existing weekly record/context, counting
   all sessions, asynchronous decisions and follow-ups. If unknown, disclose that and prepare
   a provisional digest without promising a full allowance. Best case is 120 total minutes:
   15 triage, 60 evidence/decisions, 25 feedback/actions, 10 quality/metrics, 10 contingency.
   Engineering/general maintenance is scheduled separately; actual code-PR review still counts.
2. List only the requested PR scope; fetch cheap metadata, body, changed-file scope, prior
   findings and current workflow status. Triage format, obvious duplicates and outstanding
   questions before linked-source/service investigations. New/changed/stale status depends on
   observed head/base/body, checker/policy and relevant evidence, not the label. Route code or
   infrastructure/mixed PRs to code review. Preserve historical and cleanup paths from `sprr`.
   This is reviewer routing: the existing README-only checker may still reject other files.
   Resolve check applicability in code review, without assuming routing fixed CI or waiving gates.
3. Fetch the base README once per observed base SHA. Share duplicate candidate retrieval across
   the batch: project names/URLs across open PRs and PRs closed within the last 365 days.
   Record terms, date, coverage, pagination and retrieval gaps; do not describe a partial search
   as complete. Refresh changed bases/candidate sets before acting. Judge each collision per PR.
4. Prioritize accuracy corrections in every category and substantive source candidates; order
   comparable candidates oldest-first. Select at most four detailed candidates per weekly
   batch, adjusted downward to remaining minutes, including follow-ups and genuine exceptions.
   One fully evidenced hosted service may replace a slot only after source/correction work
   when time remains; it never adds a slot or reserves capacity. Defer hosted services first
   when availability shrinks. Commercial ownership alone does not put substantive source there.
5. Prepare focused `sprr` evidence, current workflow provenance, blockers and exact actions for
   selected candidates without repeated preliminary maintainer decisions. Inspect only affected
   findings after changes; request only missing evidence for already-open PRs. Stop at a decisive
   published-rule failure or the 10–15 minute investigation boundary. Uncertain/failed retrieval
   produces one decisive evidence question or explicit deferral, not unsupported rejection.
6. Summarize unchanged/waiting-on-author/pending-CI work as counts unless a concrete action is
   needed. Changed prior submissions compete for the same slots; they do not expand the batch.
   At the time/weekly limit, carry overflow forward with no automatic acceptance/rejection and
   no SLA. At zero available time, promise no decisions/writes. Unexpected reviews use contingency,
   then displace planned work. Agent compute/preparation and human verification remain visible.
7. Present the digest below and one exact action bundle for selection. Execute only that scope
   under `sprr`; a stale action is held for affected review, not silently corrected and executed.
   Follow-ups, reapproval and result verification consume the same weekly allowance.

## Summary Output

Lead with remaining/used weekly minutes, selected count (maximum four, possibly fewer), lane
counts, and waiting/deferred counts with reasons. Then present only decision-ready candidates
(which may be evidence requests or rejection recommendations) and genuine policy exceptions:

```text
| PR | Eligibility | Priority | Readiness | Validate PR | PR Review | Proposed action |
| --- | --- | --- | --- | --- | --- | --- |
```

For each candidate, keep/link `sprr`'s common record: observed repository/PR/head/base/body,
checker and evidence date, checked/claimed/unresolved evidence, search scope/gaps, prior
findings, affected revalidation, verdict, blocker and proposed actions. Never imply that an
eligibility finding, green CI or `reviewed` label establishes readiness. Section suitability,
source/service classification and commercial evidence remain semantic judgments.

Keep notes to decisive evidence and missing questions; do not reproduce a full audit for each
waiting PR. Include exact comment text, label changes, closure effects and merge SHA/method for
every proposed action. Missing trusted snapshots are unverified; pending CI cannot authorize merge.

Ask once for selection of the listed action IDs/PR bundles, or `none`. For example:

- `bundle A and C`
- `comment 125` (only the exact listed comment, with no implied label/closure)
- `all listed actions` (only the fully specified effects)
- `none`

Apply `sprr`'s action freshness/consent contract per selected PR. Do not ask again to confirm an
unchanged selected merge. Refresh failures or material input changes hold affected actions and
require revised findings/consent; unaffected approved actions can proceed after their own checks.
Report results, partial failures and carried-forward work. Within the quality allocation, record
review minutes by task, repeated investigations, consent prompts, recovered changed submissions,
queue waits and a deferred/rejected spot-check when available. Keep sample size/case mix visible;
the pilot must assess total weekly human time and decision quality, not merely faster medians.
