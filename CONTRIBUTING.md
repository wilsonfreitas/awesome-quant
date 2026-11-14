# Contributing

Your contributions are always welcome! Please ensure your pull request meets the following guidelines.

## Evidence to Include

Help reviewers assess the submitted functionality with a short evidence block in the PR body.
Links to existing documentation are enough; do not duplicate it or run code for the reviewer.

- **Quant use case:** the concrete task, intended users, and useful result.
- **Implementation and example:** representative source implementing that task, plus one
  example or test and its expected behavior. Distinguish public functionality from a hosted
  companion; a repository URL, license, stars, or generated output alone is not implementation
  evidence. Disclose what has actually been checked versus what is claimed or unresolved.
- **Maintenance and support:** one meaningful fix, development change, documentation update,
  or other maintenance artifact; a stable maintainer handle/team and a public support route.
  A new solo project can link its initial implementation, documented limitations and support
  arrangements. No old issues, response quota, legal name, minimum stars, or minimum project
  age is required. Pseudonymous maintainers are welcome. The existing activity requirement
  below still applies; this evidence request does not change it.
- **Dependencies and access:** license, external services/data, credentials, payment or other
  restrictions, and what useful workflow is available from the public project itself.
- **Affiliation and duplicates:** your relationship to the project (or none), related existing
  entries, and searches of the README and open/recently closed PRs, with results or links.

For a **hosted service without substantive public implementation**, also link the precise
permanent-free quantitative workflow, pricing and exact limits, payment-information
requirements, and public documentation, methodology or examples. A thin SDK does not establish
that the service is open source. The [commercial rules](#commercial--proprietary-projects)
remain authoritative. For a substantive source project's required hosted dependencies, disclose
access and payment requirements and explain what the public implementation supplies. Paid data
credentials do not by themselves disqualify a substantive decoder, analysis library or standalone
client. The permanent-free eligibility gate applies to the submitted repository-less/thin-service
offering, not automatically to every external dependency. Paid hosting alone does not move a
substantive source project into the hosted-service lane. Useful standalone data clients and
open-core projects are assessed on their actual public implementation and dependencies.

For an **existing-entry correction or cleanup**, identify the inaccurate claim, broken link,
move or removal and supply evidence for that change. Use the
[cleanup rules](#audit-cleanup-pull-requests); do not resubmit an unrelated new-project dossier.
Code and infrastructure changes take a separate code-review path, not README-entry rejection.
The existing README-only `PR Review` checker may reject non-README files; this routing guidance
does not change that CI limitation. Resolve check applicability in code review rather than
treating it as project ineligibility; this policy does not waive required checks.

## Review Capacity and Outcomes

Usefulness, eligibility and merge readiness are separate judgments. A useful project solves
a concrete quantitative task; eligibility follows the published rules below; readiness also
requires current checks and manual review of this exact revision. Editorial priority determines
when a candidate receives scarce review time. Low priority is not ineligibility, and a missing
or inaccessible source is unresolved evidence, not proof of a failed rule. Reviewers ask one
decisive question rather than perform an exhaustive audit or certify trading performance.

There is **no review SLA** or promise to clear the backlog. The best-case allowance is
**120 total weekly human PR review minutes**, across all sessions and asynchronous messages:

| Activity | Minutes |
| --- | --- |
| Digest, triage and selection | 15 |
| Focused evidence review and editorial decisions | 60 |
| Feedback, action approval and result verification | 25 |
| Metrics and a deferred/rejected candidate spot-check | 10 |
| Follow-up and contingency | 10 |
| Total | 120 |

Notifications, author follow-ups, re-review, agent questions, conflicts and merge decisions
all count. Implementation, engineering oversight and general maintenance are scheduled
separately; this is not a whole-project time limit. Actual review of code/infrastructure PRs
still counts as PR review. Agent preparation and compute are recorded separately from human
verification time; moving a decision to an asynchronous message does not remove its cost.

Agents prepare an on-demand batch with at most **four detailed candidates per week**, reduced
when less review time is available. Prioritize accuracy corrections across all categories and
substantive source projects, then comparable candidates oldest-first. At most **one fully
evidenced hosted service may replace a slot** when capacity remains after source/correction
work; it never adds a fifth slot, reserves capacity, or guarantees review. Defer service review
first when time shrinks. Start with a 10–15 minute investigation boundary per candidate, not
an approval shortcut. At the time or weekly limit, request focused evidence or defer unresolved
work and carry overflow forward. Unexpected work displaces other reviews; standards and the
weekly allowance do not change. With zero available review time, promise no decisions or writes.

Unchanged submissions waiting on authors or CI are summarized without repeated investigation.
Changed submissions return for review of the affected findings, including PR-body-only edits.
The `reviewed` label alone never establishes a current review or approval. Maintainers approve
exact comment text, label changes, closures and merge targets in one explicit action-bundle
selection; that consent is sufficient once for the unchanged scope. Relevant inputs, workflow
evidence and duplicates are refreshed before execution. Material changes hold affected actions
for renewed review and consent. Passing checks or a classification label cannot authorize writes.

These intake and scheduling rules apply going forward, including the next review of already-open
PRs. For those PRs, reuse supplied evidence and request **only missing evidence** needed to decide
the submission; absence of the new template is not a rejection reason. There is no mass re-review,
mass rejection or purge of existing listings. Correction requests remain in the correction queue
regardless of category. Existing duplicate rules, historical exceptions, cleanup rules, permanent
free-tier requirements and the 12-month activity requirement remain in force. Maintenance
eligibility is unchanged by this process policy.

## Entry Format

Each non-commercial entry must include one or more backtick-delimited tags and follow one of
these formats. Tags work like a compact tag cloud: use concise terms that help readers
understand the project, such as programming languages, runtimes, protocols, interfaces, data
types, or domains.

### Single tag

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` - Short description ending with a period.
```

Tags are not limited to programming languages. For example:

```markdown
- [Project Name](https://github.com/owner/repo) - `MCP` - Short description ending with a period.
```

### Multiple tags

List each tag separately in adjacent backticks:

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` `MCP` - Short description ending with a period.
```

### Project with website and GitHub repo

For projects that have a dedicated website, link to the site and append the GitHub repo in the description:

```markdown
- [Project Name](https://project-site.com) - `Python` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

### CRAN project

Link to the CRAN package page. If the project has a GitHub repo, append it after the description:

```markdown
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period.
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

### PyPI project

Link to the PyPI package page. If the project has a GitHub repo, append it after the description:

```markdown
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period.
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

### General rules

- Use `https://` URLs only.
- GitHub repositories containing substantive implementation are strongly preferred and are a
  major positive relevance signal.
  Projects with a verifiable GitHub repository are easier to evaluate for source availability,
  documentation, activity, maintenance, and community adoption, and they receive automated
  tracking of stars, activity, and archive status on
  [the awesome-quant site](https://wilsonfreitas.github.io/awesome-quant/).
- A public GitHub repository containing the substantive implementation is preferred. Use it
  as the main URL, or append the exact `[GitHub](https://github.com/owner/repo)` suffix when
  the project has a separate website. Repository-less commercial services are considered only
  under the eligibility rules below. A substantive GitHub repository mentioned in either place
  receives the same relevance consideration; repository existence alone does not establish
  commercial eligibility or functional-section placement.
- Use short, meaningful tags. Each concept must have its own backtick pair; for example,
  use `` `Python` `C++` `` rather than `` `Python, C++` ``.
- The description must end with a period (before the `[GitHub]` link, if present).
- Keep descriptions concise — one sentence.

## Quality Requirements

- **Active source-backed projects**: Provide substantive implementation, a clear README with
  usage examples, and evidence of meaningful maintenance within the preceding 12 months.
  Examples include a relevant fix, compatibility update, release, substantive documentation
  improvement, or engagement that resolves a reported problem. Link one representative
  artifact and identify the responsible maintainer or team through a stable public handle
  and support route. A recent push, bot commit, license, or README alone is not proof.
- **Mature, low-change software**: A project without recent development may still qualify
  when the contribution supplies current compatibility or reproducibility evidence, known
  limitations, and an accountable support route. The reviewer records the specific evidence
  and exception rationale; a submitter's claim alone does not grant an exception. If that
  evidence is missing, request it or consider historical placement rather than automatically
  rejecting or removing the project because of its age.
- **History and identity**: Public development and release history provide context; there is
  no minimum repository age, star count, team size, or legal-name requirement. A young or
  migrated repository is not evidence of immaturity. Solo and pseudonymous maintainers can
  demonstrate responsibility through their work and engagement.
- **Educational resources**: In Reproducing Works, Training & Books, evaluate the concrete
  learning/reproduction purpose, provenance, instructions, and documented environment and
  limitations. Fixed research artifacts need not receive continuous commits. Executable
  examples need reproducibility evidence for the stated environment; a book or paper needs
  a reachable authoritative source. This does not exempt ordinary active software from
  maintenance assessment or allow archived repositories outside the historical category.
- **Historical & Archived Projects**: This category is the narrow exception to the active
  activity and archive-state requirements. An entry must use `Historical` plus a language or
  runtime tag, link to reachable substantive source or documentation, state a specific
  historical, educational, or foundational reason to retain the project, and clearly disclose
  that it is archived or unmaintained. It is not for thin wrappers, tutorials, generated data,
  marketing material, unsupported SDKs, or duplicate implementations.
- **Repository-less commercial services**: See the permanent-free-tier, public-documentation,
  and transparency rules in the commercial section below.

The automated reviewer reports the latest default-branch **committer** date as a preliminary
recency screen. An old or unavailable date triggers a manual evidence assessment; a recent
date does not verify that the work was meaningful. Check relevant releases, fixes, examples
or support when making the editorial decision. Archived source still requires historical
placement, apart from the documented same-section cleanup exception. Passing deterministic
checks never approves a maintenance exception or establishes merge readiness.

### Editorial quality and upkeep

Describe the quantitative task and concrete capability in factual language. For a benchmark
claim, provide the compared versions, workload/data, metric, environment and reproducible
methodology; otherwise use a factual capability description without the unsupported number
or superiority claim. Reviewers do not need to reproduce an exhaustive benchmark suite.

Use the weekly audit as leads for focused correction batches. Recheck changed or genuinely
unresolved evidence, retaining attributable prior decisions; HTTP restrictions and temporary
errors alone do not justify removal. Review work for corrections and guide updates belongs
in the same weekly PR review budget, not an additional mandatory deep audit. A relevant
upstream change or reported error can trigger a guide update. Broader catalogue maintenance
and engineering have separately scheduled effort.

The [backtesting selection guide](docs/choosing-backtesting.md) illustrates task-oriented
comparison and records its sources and limits. It is a starting point, not a ranking or a
guarantee of suitability.


## Commercial & Proprietary Projects

Public repositories containing substantive implementation remain preferred. A commercial or
proprietary project without such a repository qualifies only when it has a meaningful permanent
free tier that provides useful quantitative-finance functionality without requiring payment
information. Trials, demos, waitlists, and paid-only products do not qualify.

Commercial services without substantive public source—including those with only a thin SDK,
integration, examples, generated-data, or marketing repository—are repository-less for every
eligibility check. They must publish pricing and free-tier limits, as well as public documentation,
methodology, or usage examples. Their entries must use a stable HTTPS URL without affiliate or
tracking parameters, have a concise, factual, non-promotional description, and be placed in the
**Commercial & Proprietary Services** section. Use the service name and website as the main
link; when a supporting repository exists, append it as the exact `[GitHub](...)` suffix.
Describe the service and relevant free-tier limits, not merely its SDK. Backtick tags are
optional in that section. For example:

```markdown
- [Project Name](https://project.example) - Concise factual description ending with a period.
- [Service Name](https://service.example) - Factual service description with relevant free-tier limits. [GitHub](https://github.com/owner/client)
```

Reviewers inspect representative source files to establish whether advertised functionality is
implemented publicly or merely accessed through a proprietary service, and follow linked service
documentation and pricing pages. Small size, few stars, or recent creation alone do not make a
repository thin. An open-source SDK license does not make the service open source; substantive
public implementation may qualify for a functional section even with a paid hosted version.

Only a repository containing substantive implementation supports placement in a functional
section. Commercial submissions without a qualifying permanent free tier—including paid-only,
trial-only, demo-only, and waitlist-only offerings—are `REJECT`. Reserve `NEEDS CHANGES` for
correctable evidence or disclosure, wording, URL, documentation, or placement defects when the
underlying offering can qualify.

## Section Placement

The README is organized by **category** (not by language). Add your entry under the appropriate category heading (`##`). The available categories are:

- Numerical Libraries & Data Structures
- Financial Instruments & Pricing
- Technical Indicators
- Trading & Backtesting
- Portfolio Optimization & Risk Analysis
- Factor Analysis
- Sentiment Analysis & Alternative Data
- Time Series Analysis
- Market Data & Data Sources
- Prediction Markets
- Calendars & Market Hours
- Visualization
- Excel & Spreadsheet Integration
- Quant Research Environments
- Cross-Language Frameworks
- Reproducing Works, Training & Books
- Commercial & Proprietary Services
- Historical & Archived Projects
- Related Lists

For example, if your project is a Python backtesting library, it goes under `## Trading & Backtesting` (not under Technical Indicators or another category).

If no existing category fits, suggest a new one in your PR description.

## Multiple Related Projects Per PR

**Preferred:** One project per pull request for clarity and focused reviews.

**Acceptable:** Multiple closely related projects in a single PR if they share a common theme or data source. Examples:
- Multiple data sources from the same market or exchange (e.g., all NSE/BSE tools for Indian markets)
- Multiple tools from the same author with complementary functionality
- Multiple APIs/SDKs for the same service or data provider
- Related packages addressing a specific domain gap (e.g., UK company identifier validators)

When submitting multiple projects:
- Explain the relationship and rationale in the PR description
- Ensure each entry is placed in the correct section
- Avoid creating duplicate entries within the same README file
- All entries must meet quality and format requirements independently

### Audit cleanup pull requests

Keep cleanup batches focused on existing entries and explain each update, move, or removal
with supporting evidence in the PR description. A cleanup batch may change more than five
entries or only remove entries. The reviewer identifies cleanup from the diff: every added
entry line must correspond one-to-one to a removed entry for the same project. Unrelated new
projects belong in a separate contribution PR; ordinary contributions retain the limit of
five added entry lines. Existing indented non-entry references may receive a canonical
GitHub repository URL repair only: exactly one HTTPS repository link may change, the old and new links must
resolve to the same immutable GitHub repository ID, and all surrounding text, indentation,
category, parent entry occurrence, and relative position must remain unchanged. Pair each repair with its existing
reference; new references, extra copies, removals, and other non-entry prose or heading
changes are outside cleanup scope. Offline validation checks the repair structure;
`PR Review` additionally verifies repository identity.

Changed entries still undergo format, section, HTTPS, duplicate, primary-link reachability,
and repository/documentation checks. Within the same section, cleanup does not reapply the
new-project activity/archive requirements to an unchanged repository, or require a previously
repository-less entry to acquire a repository. Replacement repositories and section moves
receive the normal source and activity checks. These limited exceptions allow legacy links
to be repaired; they do not establish that the entry meets every current eligibility rule.

Removed entries receive structural checks, without probing the unavailable resources being
removed. Maintainers must verify the removal evidence, replacement searches, historical
eligibility, and commercial status as applicable. A passing automated review reports
`CHECKS PASSED` and requires maintainer review; it does not approve or merge a cleanup.

## Before Submitting

1. Search the existing list to make sure the project is not already included.
2. Search previous Pull Requests (open and closed) to avoid duplicates.
3. Make sure the entry format matches exactly — our parser relies on it.

## Required Pull Request Workflows

Every pull request that adds, updates, or removes a README entry must pass both required GitHub Actions
workflows:

- **`Validate PR`** checks the added README entries against the parser and formatting rules,
  then verifies that the static site can be generated.
- **`PR Review`** runs the repository's read-only automated review, including contribution,
  project-quality, URL, repository, activity, documentation, and existing-README duplicate
  checks.

Both workflows must pass on the latest pull request revision before the project can be accepted.
A success from an older revision does not count. If either workflow is failed, pending, cancelled,
missing, or stale, the pull request is not eligible for approval or merge. Fix any reported issues
and push a new revision so the required workflows run again.

For `Validate PR`, use the latest attempt for the current head SHA; a newer pending attempt
supersedes an older success. For `PR Review`, a trusted log/job-summary snapshot must identify
the repository and PR, observed head/base/merge-base SHAs, PR-body and title SHA-256,
trusted checker revision, source digest, clean-source status and observation time.
The head, base, body and title must match the current inputs, and the checker
revision must be the trusted implementation used for that run. A `pull_request_target` workflow
SHA alone does not identify the submitted head. Missing, mismatched or untrustworthy provenance
is **unverified**, even when the check is green; request a fresh trusted run. Local validation
can supply findings but cannot waive either required workflow gate.
The full contribution diff is reconstructed from immutable merge-base/head contents; current
base contents remain the duplicate-check reference. A partial API patch cannot establish scope.
Local modified checker sources are identified explicitly and cannot substitute for clean CI.

Passing both workflows is necessary but not sufficient. Maintainers also review relevance,
description quality, section placement, repository substance, commercial eligibility, and
duplicates in other open or recently closed pull requests.

## Rejection and Corrections

Reviewers recommend rejection for confirmed failures of the published eligibility rules,
including:

- Multiple unrelated projects added in a single PR without a clear grouping rationale.
- Duplicate of an existing entry or a recently closed PR.
- Project is archived or abandoned, unless it meets the documented
  **Historical & Archived Projects** eligibility criteria.
- Empty PR description.

Correctable format, wording, placement or missing-evidence defects receive a focused change
request. Uncertain service access or failed evidence retrieval is not a confirmed rejection.
Confirmed paid-only, trial-only, demo-only and waitlist-only services still fail the commercial
rules. Every comment, label, closure or merge requires explicit approval of its exact action;
there are no automatic public actions.
