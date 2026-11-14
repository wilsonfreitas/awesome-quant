---
name: sprr
description: Use when the user asks to review, validate, comment on, label, close, or merge one specific awesome-quant README-entry pull request, including corrections, cleanup, "sprr", "review PR", "check PR", or "validate contribution".
---

# SPRR: Single PR Reviewer

Review one README-entry contribution, correction or cleanup. Use
[CONTRIBUTING.md](../../../CONTRIBUTING.md) as the public policy authority and follow
[its capacity policy](../../../CONTRIBUTING.md#review-capacity-and-outcomes).
Keep eligibility, editorial priority and merge readiness separate.

## Hard Rules

1. Review only the PR number the user requested. If no PR number is given, ask for one.
2. Use GitHub MCP tools for PR operations. Do not use `gh` for PR review, comments, labels, closing, or merging.
3. Do not modify the PR until the user explicitly selects the exact action bundle below.
4. Present findings and exact actions before consent; one explicit selection authorizes that
   unchanged scope once, including an explicitly listed merge. Do not ask for identical consent again.
5. Recheck freshness immediately before acting; material changes invalidate affected consent.
6. Enforce `CONTRIBUTING.md` and `AGENTS.md` strictly for new entries, using the
   sentence-count interpretation in the Validation Checklist below.
7. Both `Validate PR` and `PR Review` must pass before returning `APPROVE`.

If GitHub MCP tools are unavailable, report that PR operations are blocked and point the user to `docs/codex-setup.md`.

## Workflow

1. Fetch PR details/body, current head and base SHAs, files, labels, comments, diff and existing
   attributable review records with GitHub MCP. Record the evidence date and body digest below.
   A `reviewed` label alone is never a skip or pass. Apply the legacy CI transition below
   when provenance predates snapshots; otherwise missing provenance is unknown, not passed.
   Reassess only what is needed. Do not silently ignore a body-only edit.
2. Cheap triage first: classify new entry, accuracy correction, cleanup, historical, or
   code/infrastructure; inspect scope, format, duplicate candidates and outstanding findings.
   Route code/infrastructure or mixed changes to separate code review rather than README-entry
   rejection. Reuse batch retrieval from `bprr` with its base SHA and search scope recorded.
   The existing README-only checker may reject non-README files; routing is reviewer guidance,
   not a CI fix. Resolve check applicability in code review without waiving required gates.
3. Compare current inputs and evidence with the prior review. New, changed or stale submissions
   re-enter relevant review. Unchanged waiting-on-author/pending-CI work gets a short status;
   no repeat investigation without new evidence. No mass re-review/rejection. For already-open
   PRs request only missing evidence, not completion of the new template for its own sake.
4. Fetch both latest required workflow attempts and apply the provenance rules below, including
   the legacy transition when applicable. A changed head/base/body or checker requires affected
   evidence to be revalidated under the applicable path. Preserve useful manual
   findings independently of a missing check; pending CI blocks readiness, not eligibility.
5. Revalidate affected findings using the table below; reuse unchanged attributable findings
   with their source links, date and limits. Refresh live facts when stale, changed, unavailable,
   or needed for an action. No fixed age expiry is introduced. Stop at a decisive published-rule
   failure; do not research pricing after an independently confirmed duplicate, for example.
   For a selected candidate blocked by a README conflict, prepare the mechanical resolution
   below before presenting actions; do not automatically send integration work to the author.
6. For new, changed, stale or missing source findings in selected candidates, inspect one
   implementation path, one example/test and one maintenance artifact as relevant to those
   findings. Reuse attributable unaffected evidence. Record checked/claimed/unresolved.
   Apply linked-service research only
   when required to assess the submitted functionality. Use a 10–15 minute investigation
   boundary within the remaining weekly allowance. At uncertainty/timebox limits draft one
   decisive evidence question or defer; never turn retrieval failure into a rejection.
7. If mechanical validation is not established by trusted current CI, reproduce it only when
   useful for a selected candidate. Save/reconstruct the PR diff and validate added entries with:

```bash
uv run python scripts/validate_readme.py --diff-from <base-ref>
```

If a base ref is not locally available, apply the same checks manually from the fetched diff.
Local results provide findings, not a substitute for either workflow gate. Do not execute
contributor code or start an exhaustive audit. Complete cross-PR duplicate searches before
readiness: names and URLs across open PRs and PRs closed within the last 365 days, plus current
base README. Record queried terms, scope, date, results and pagination/retrieval gaps. Shared
candidates save retrieval, not per-entry judgment; incomplete coverage is unresolved.

| Changed input | Findings to revisit |
| --- | --- |
| Wording only | Accuracy, factual claims and concision; retain unrelated source findings. |
| PR body only | New evidence, affiliation/access claims, relatedness and outstanding questions; refresh body-bound CI. |
| Main/repository URL, implementation or hosted dependency | Substance, relevance, source/service classification, access eligibility, duplicates and reachability. |
| Section move or historical status | Semantic placement and applicable source/activity/historical rules. |
| Base README or checker/policy | Affected duplicate/mechanical/policy findings and required workflow evidence. |
| Mechanical conflict caused by base advancement | Preservation of base content and the reviewed contribution, duplicates, section and new-revision CI; retain unaffected editorial evidence. |
| Unchanged evidence waiting on author/CI | Summarize blocker; no repeated full review. |

Historical entries use CONTRIBUTING.md's `Historical & Archived Projects` exception rather
than ordinary activity/archive rejection. Cleanup is identified from the diff: one-to-one
same-project replacements or removals, with only the documented nested-reference repair
exception. Preserve same-section unchanged-repository activity/archive and repository-less
exceptions; replacement repositories and section moves receive normal checks. Verify removal
evidence, replacement searches and historical/commercial status manually. `CHECKS PASSED`
is not eligibility or merge approval. Read the public cleanup rules rather than inventing
a five-entry rejection for a valid cleanup batch.

## Mechanical Conflict Preparation

Prepare only selected candidates, in an isolated local directory/worktree. Fetch the actual
current base branch tip, PR head and common ancestor; a PR's recorded base SHA may be older
than the branch tip. Reconstruct the three-way conflict without executing contributor code.

A conflict is mechanical only when the reviewed contribution can be preserved exactly alongside
all current-base content, without an editorial choice. For independent additions at the same
position, retain both entries in their intended section. Never blindly choose ours/theirs.
Conflicting descriptions, URLs, placement, duplicates, removals or unrelated files require
affected editorial/code review and a revised proposal; they are not mechanical repairs.

Before proposing publication:

1. Show the resolved diff against the current base. Prove that the complete resulting tree is
   the current base plus only the previously reviewed contribution: no lost entries, incidental
   edits or changes outside the approved scope. Recheck affected duplicates, placement and format.
2. Record repository, target fork/branch, original head, current base, common ancestor, exact
   patch and resolved tree/content digest. Reuse unaffected source/maintenance findings.
3. Check tool capability and fork write permission. Missing permission metadata is unknown,
   not a denial or a grant. If access cannot be established, keep publication blocked and supply
   the prepared patch; any message to the author needs its own approved exact text.
4. Prefer merging the observed base into the contributor branch with the contributor head as
   first parent, followed by a guarded fast-forward update. Preserve history; do not force-push,
   replace the PR or change the contribution as an implicit conflict repair.

Local preparation needs no PR-write consent and does not establish merge readiness. Publication
and any conditional merge must be explicitly included in the selected action bundle below.
After publication, require both workflows for the resulting revision under the normal provenance
rules. Old-head success and local validation cannot satisfy these gates. Do not attribute a CI
failure to the conflict without evidence.

Integrate selected PRs sequentially, refreshing the base before each one. If inputs change,
reassess affected evidence and the prepared result; do not silently expand an approved patch or
enter an unbounded repair/retry loop. Carry blocked work forward within the human review budget.

## CI Evidence Rules

For `Validate PR`, use only the latest attempt whose commit SHA exactly matches the current
head SHA. A newer queued or pending attempt supersedes an older successful attempt for that
SHA. `Validate PR` is head-bound; it does not require a PR-body snapshot. The body/base/checker
snapshot contract below applies to `PR Review`.

| Current-head result | Review behavior |
|---|---|
| `success` | Accept current-head parser format, tags, separators, final period, HTTPS and GitHub-link syntax. Base-README duplicates must also be established against the current base. Do not repeat established checks. |
| `failure` | Inspect the failing job or step. Return `NEEDS CHANGES` when validation failed; if another step failed or details are unavailable, reproduce mechanical validation before deciding. |
| queued, pending, awaiting approval | Report the review as incomplete and do not return `APPROVE`. |
| skipped, cancelled, missing | Report the review as incomplete and do not return `APPROVE`; reproduce mechanical validation only to provide useful findings. |
| success on an older SHA | Report the result as stale and do not return `APPROVE`; require a successful attempt for the current SHA. |

CI never replaces inspection of the diff or the manual checks below. A successful check confirms
only mechanical rules; it does not establish tag meaning or concision, description quality,
relevance, semantic section suitability, commercial classification, repository quality,
commercial free-tier eligibility or transparency, URL tracking, cross-PR uniqueness, or
multi-project relatedness. CI cannot establish any of these manual criteria. Search open PRs and PRs
closed within the last 365 days for duplicate names and URLs.

`PR Review` runs on `pull_request_target`: its workflow SHA is not proof of the inspected head.
Use the latest associated attempt, including a newer pending/failing attempt. For a checker
that supports snapshots, require its trusted inspected-input snapshot. Never fall back to an
older success. A missing/untrustworthy stamp or mismatched head/base/body/checker from such a
checker is `UNVERIFIED`, even on a green run; request a fresh trusted run. For a checker that
predates snapshots, apply the legacy CI transition below. If failure reports a PR defect,
return `NEEDS CHANGES` or `REJECT` under the published
rule; infrastructure/retrieval failures leave readiness incomplete. Queued/pending/awaiting
approval is `PENDING`; cancelled/skipped/missing is `UNVERIFIED`. None allows `APPROVE`.

## PR Review Provenance

Read the `Review snapshot` from trusted CI logs/job summary, not contributor-supplied text.
The snapshot contract is:

| Field | Meaning |
| --- | --- |
| `repository` | Exact base owner/repository. |
| `pr_number` | PR actually reviewed. |
| `head_sha` | Submitted head used for diff/head reads. |
| `base_sha` | Base used for diff/base README reads. |
| `merge_base_sha` | Common ancestor used with the head to reconstruct the complete contribution diff; current-base README is checked separately for duplicates. |
| `body_sha256` | SHA-256 of the exact UTF-8 PR body, with null treated as empty. |
| `title_sha256` | SHA-256 of the exact PR title used in the report. |
| `checker_revision` | Trusted checked-out checker commit, obtained by the runner, not a submitter field. |
| `checker_sources_sha256` | Digest of the checker and its local implementation dependencies actually inspected. |
| `checker_clean` | Whether those sources match the recorded commit; must be true for authoritative CI evidence. |
| `observed_at` | UTC observation time; provenance, not an equality input. |

Match repository, PR, head, base, body and title digests against freshly fetched PR inputs. Establish
checker revision from the trusted checkout/run; if it changed since earlier evidence, revalidate
affected findings with the applicable trusted checker. The run must have re-fetched inputs
before success and failed/incompleted on changes or failed refresh. Require `checker_clean` to
be true and source attribution to be present; dirty local findings are not authoritative CI
evidence. The checker must also invalidate its result if its local sources change during review.
Observation time alone
cannot establish freshness. Runs from checkers predating this stamp use the transition below.
Do not equate a target workflow commit with submitted code.

## Legacy CI Transition

Missing snapshots alone do not block successful checks produced by the checker before snapshot
support. Determine this from the trusted checkout revision and checker source, not the age of
the PR or a contributor assertion. This transition preserves both workflow gates:

1. Require the latest relevant attempts of both workflows to have succeeded for the current
   PR head. Establish the PR/head association from trusted Actions metadata and available logs;
   a `pull_request_target` workflow SHA alone is insufficient. Never use an older success over
   a newer pending/failing attempt or treat a success for an older head as current.
2. Inspect the current complete diff and reconcile it with the successful run's scope. Check
   current body/title evidence, current-base duplicates and affected policy/external facts.
   Missing historical body hashes do not require reconstructing an unavailable old body:
   assess its current claims directly. Reuse attributable unaffected manual findings.
3. Record run/attempt links, current head/base/body/title, trusted checker revision, evidence
   establishing the run's association, manual reconciliation and remaining gaps. Report
   `PR Review: PASS (legacy CI + manual reconciliation)` and
   `Inspected inputs: MANUALLY RECONCILED` only when these checks establish coverage. Do not
   invent a snapshot or claim the old CI assessed current body/base/policy inputs.
4. When association, coverage or a material subsequent change cannot be resolved within the
   review budget, hold readiness as `UNVERIFIED` and request a fresh run using the current
   trusted checker. Verify its actual checkout and snapshot: rerunning a historical job can
   reuse the old checker. This is maintainer CI work, not an automatic request for an author
   rebase, empty commit, template rewrite or another public comment.

An attributable legacy success with complete manual reconciliation can support `APPROVE`
after the normal editorial review. It needs no separate exception approval; the exact action
bundle still requires user consent. A checker that supports snapshots but omits or mismatches
one cannot use this transition. Apply it only to selected candidates, without a backlog-wide rerun.

## Validation Checklist

For each selected entry, apply the relevant rules below to new or affected findings; reuse
attributable unchanged evidence and preserve the cleanup exceptions above:

- It matches `^\s*- \[(.*)\]\((.*)\) - (.*)$`.
- New non-commercial entries include one or more backtick tags followed by ` - `. Treat these
  as a compact tag cloud: accept concise languages, runtimes, protocols, interfaces, data
  types, and domain terms.
- Separate concepts use adjacent tags, such as `` `Python` `C++` `MCP` ``; do not reject a tag
  merely because it is not a programming language.
- Description ends with a period before optional `[GitHub](...)`.
- Treat `CONTRIBUTING.md`'s "one sentence" wording as concision guidance, not a sentence-count
  gate. Accept two or more short sentences when the overall description remains concise, factual,
  relevant, and non-promotional. Never return `NEEDS CHANGES` solely because of sentence count;
  request wording changes only for actual quality problems such as verbosity, repetition,
  unsupported claims, promotional language, or poor readability.
- URLs use `https://`.
- Optional GitHub link uses `[GitHub](https://github.com/owner/repo)`.
- Section placement matches the project's purpose.
- Distinguish repositories containing substantive implementation from thin SDK, integration,
  examples, generated-data, or marketing repositories.
- Hosted proprietary products without substantive public source are under
  `Commercial & Proprietary Services`, even when a thin repository exists.
- For repository-less commercial entries, verify a useful permanent free tier for quantitative
  finance that requires no payment information and is not a trial, demo, or waitlist.
- Treat a commercial service with only a thin SDK, integration, examples, generated-data, or
  marketing repository as repository-less for every eligibility check.
- Verify that these commercial entries publish pricing and free-tier limits plus public
  documentation, methodology, or usage examples; use a stable HTTPS URL without affiliate or
  tracking parameters; and have a concise, factual, non-promotional description.
- Project name and URLs are not duplicates of existing README entries.
- A verifiable GitHub repository containing substantive implementation, mentioned as the main URL
  or exact `[GitHub](...)` suffix, is a strong positive relevance signal. Repository existence
  alone does not establish commercial eligibility or functional-section placement.
- GitHub projects are checked for source availability, activity, archived status,
  documentation, and community evidence. GitHub relevance does not waive duplicate, format,
  or quality checks.
- Multiple projects in one PR are closely related and explained in the PR body.

## Repository Substance and Linked Services

For a selected entry with new, changed or stale source findings, inspect what its public
implementation provides:

1. Inspect representative implementation files behind the advertised functionality. A README,
   license, tests, file count, or stars alone do not establish substance.
2. Trace whether core functionality is implemented publicly or depends on a proprietary service.
   Identify code that only calls a vendor API, integrates a service, downloads generated output,
   or provides examples or marketing. External dependencies alone do not make a project thin;
   assess where the advertised functionality is implemented.
3. For required hosted dependencies, verify the disclosed access requirements and what useful
   functionality the public implementation supplies. Paid data credentials do not by themselves
   disqualify a substantive decoder, analysis library or standalone client. Apply the permanent-free,
   no-payment-information eligibility rules only when the submitted offering is a hosted service
   without substantive public implementation, including a thin service SDK. Follow relevant
   service documentation/pricing for that assessment; do not investigate unrelated paid hosting
   for an independently useful public implementation.
4. Report concrete evidence: representative source-file links, API dependencies, and relevant
   service/pricing/documentation links. State unavailable or inconclusive evidence explicitly.
   Small size, few stars, or recent creation alone do not imply poor quality or commercial status.

Solo and pseudonymous maintainers need no legal-name verification, old issues or response quota.
Use fixes, development, documented limitations and a support route as maintenance evidence,
including initial implementation for new projects. Do not infer authenticity from identity,
avatars or apparent AI use. Useful standalone data clients and open cores are assessed by their
actual public functionality; API use alone does not make implementation thin. Retain the current
12-month activity rule from CONTRIBUTING.md; maintenance eligibility is unchanged here.

When a repository mainly supports a qualifying commercial service, place the entry in
`Commercial & Proprietary Services`. Use the service name and stable service website as the main
link, and retain the repository only as the exact `[GitHub](...)` suffix:

```markdown
- [Service Name](https://service.example) - Factual service description with relevant free-tier limits. [GitHub](https://github.com/owner/client)
```

Describe the service, not merely its SDK. An open-source client license does not make the hosted
service open source. Substantive public implementation can qualify for a functional section even
when its maintainers also sell a hosted service.

- Qualifying service with incorrect placement or a thin repository as its main link:
  `NEEDS CHANGES`, with a proposed corrected README entry.
- Confirmed paid-only, trial-only, demo-only, waitlist-only, or otherwise non-qualifying free
  access: `REJECT`; moving the entry does not fix eligibility.
- Insufficient evidence of repository substance or service eligibility: `NEEDS CHANGES`, naming
  the missing evidence without claiming that the service qualifies.

## Verdicts

Use these verdicts:

- `APPROVE`: both required workflows pass and the entry is ready to merge after manual review.
- `INCOMPLETE`: the assessment could not reach a decision within the timebox/weekly limit, or
  checks/search coverage remain pending or unverified. Preserve established eligibility findings;
  never infer rejection from uncertainty or low editorial priority.
- Sentence count alone does not affect the verdict; evaluate description quality using the criteria
  in the Validation Checklist.
- Commercial submissions without a qualifying permanent free tier—including paid-only,
  trial-only, demo-only, and waitlist-only offerings—are `REJECT`.
- Reserve `NEEDS CHANGES` for correctable evidence or disclosure, wording, URL, documentation, or
  placement defects when the underlying offering can qualify.
  A precise missing-evidence request may use this verdict while eligibility remains
  `NEEDS EVIDENCE`; it does not assert that the service qualifies.
- Other `REJECT` cases include duplicates, unrelated multi-project PRs, empty PR descriptions,
  archived or abandoned projects unless they qualify under CONTRIBUTING.md's
  `Historical & Archived Projects` exception, and other hard rejections.
- Cleanup follows CONTRIBUTING.md's limited exceptions, with manual review still required.

## Output Shape

Keep this record in existing review records/digests, not a new database. Record reused findings
and their attribution; mark unknowns explicitly. A bulk digest may link to these details:

```text
PR #<number>: <title>
Observed: <repository>#<pr_number> head=<head_sha> base=<base_sha>
Body: <body_sha256>; checker=<checker_revision or UNVERIFIED>; evidence date=<observed_at>
Prior review: <record link/date/inputs or UNKNOWN>; changes since review: <affected findings>
Scope: <files, lane, entries>; duplicate search: <terms/scope/date/results/gaps>
Eligibility: QUALIFIES | FAILS PUBLISHED RULE <rule/evidence> | NEEDS EVIDENCE
Priority: <reason; distinct from eligibility>
Readiness: READY | BLOCKED <specific blocker>
Integration, when needed: <mechanical or editorial; preserved content; patch/tree digest; target branch and permission; observed base/head; publication/CI blockers>

Automated validation:
- Validate PR: PASS | FAIL | PENDING | UNVERIFIED
- PR Review: PASS | PASS (legacy CI + manual reconciliation) | FAIL | PENDING | UNVERIFIED
- Inspected inputs: MATCH | MANUALLY RECONCILED | STALE | UNVERIFIED; run/attempt/log links: <links>
- Legacy transition, when applicable: <trusted checker revision, PR/head association, current-input reconciliation and gaps>
- Mechanical checks: accepted from CI | reproduced locally | incomplete

Findings:
- Checked: <entry, finding, representative links, date, scope/limits>
- Claimed: <unverified contributor assertions>
- Unresolved: <one decisive question or deferral reason>

Verdict: APPROVE | NEEDS CHANGES | REJECT | INCOMPLETE
Proposed actions: <exact bundle below, or wait/defer>
```

Waiting/unchanged/pending work is summarized without a full dossier unless action is needed.
At most four detailed candidates fit the weekly batch; single-PR reviews and follow-ups draw
from the same allowance, not a fresh quota for every invocation.

## Exact Action Bundle and Freshness

Present the exact PR/revision/body-bound actions together: full comment text, labels to add/remove,
closure effects, and merge head SHA/method (squash by default). A question recommending comment
alone does not authorize a label, closure or merge. Add `reviewed` only after the user approves
the listed review comment and label change; it never establishes eligibility or freshness.
Classification labels cannot imply approval.

Ask for one explicit selection of that concrete bundle. A clear selection authorizes only the
listed actions for the observed inputs, once; do not ask again for identical approval, including
a listed merge. Ambiguous selections authorize no unstated effects.

For a prepared mechanical resolution, the bundle may explicitly authorize publication plus a
conditional merge before new CI exists. Include the exact resolution and inputs recorded above,
publication method, merge method, and conditions: verify the published commit's parents and full
tree against the approved result, both latest workflow gates/provenance must pass, all affected
manual findings must be resolved, and no material unapproved input change may have occurred.
Record the resulting commit SHA and use it as the expected-head merge guard. The intended head
transition to this verified result is already authorized; it does not itself require another
consent prompt. A different result or unexpected head/base/body/title/policy change holds affected
actions for renewed review/consent. Keep readiness BLOCKED and verdict INCOMPLETE until the gates
pass; conditional authorization is not an APPROVE verdict or permission to bypass CI.

Immediately before each selected PR's actions, refresh head/base/body, relevant external evidence,
both latest required attempts/provenance and README/cross-PR duplicates. On failed refresh, hold
the action as unverified. Except for the verified head transition explicitly authorized above,
a material change invalidates affected findings and consent: hold that
PR, review the changed evidence, and obtain approval for the revised bundle within available
time. Unaffected PRs may proceed under their original selection after their own refresh; overflow
carries forward. Pending CI prevents merge; a precisely approved evidence-request comment may
still proceed if its basis is unchanged. Use the merge API's expected-head guard so a race cannot
merge unreviewed code. If the tool cannot guard the head, hold the merge.

Execute only selected actions through GitHub MCP, rechecking after intervening changes. Report
actual results, partial failures and held actions; do not retry completed writes blindly or
claim the whole bundle succeeded. No live writes occur during scenario walkthroughs.
