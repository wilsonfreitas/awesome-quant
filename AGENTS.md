# AGENTS.md

## Project Overview

`awesome-quant` is a curated list of quantitative finance libraries, packages,
and resources. The source of truth is `README.md`; the static website is
generated into `site/index.html`.

The README is organized by category headings (`##`), not by language headings.
Project metadata is stored in inline backtick tags inside each entry. Tags commonly identify
languages, but may also identify runtimes, protocols, interfaces, data types, or domains.

## Architecture

1. `README.md` contains curated entries.
2. `parse.py` parses `README.md`, enriches GitHub/CRAN/PyPI metadata, and writes
   `site/projects.csv`.
3. `site/generate.py` parses `README.md` for local previews by default. Explicit
   `--source csv` reads enriched `site/projects.csv`; both write `site/index.html`.
4. `.github/workflows/build.yml` runs the parser and generator, then deploys
   `site/` to GitHub Pages.

## Work Tracking and Planning

- Linear is the system of record for issues, prioritization, specifications,
  designs, and implementation plans.
- Manage GitHub-originated issues through their synced Linear issues. Do not
  create a second internal tracker for the same work.
- Store each specification, design, and implementation plan as a Linear
  document attached to the corresponding Linear issue. Do not add task-specific
  planning documents to the repository.
- Keep repository documentation for durable project and user documentation only.
- GitHub remains the public contribution surface for pull requests and public
  issue discussion; use Linear for internal status, priority, and planning.

## Commands

```bash
# Install deps (requires Python 3.11+)
uv sync --no-install-project

# Validate README entries changed in a PR
uv run python scripts/validate_readme.py --diff-from origin/main

# Validate the full README; legacy format/duplicate/URL issues are warnings by default
uv run python scripts/validate_readme.py

# Run parser (requires GitHub token)
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py

# Generate a preview from the current README (no token required)
uv run python site/generate.py

# Generate production HTML after parse.py has written enriched CSV
uv run python site/generate.py --source csv
```

## Entry Format

The critical parser regex is:

```text
^\s*- \[(.*)\]\((.*)\) - (.*)$
```

Accepted entry examples:

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` - Description ending with a period.
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Description ending with a period.
- [Project Name](https://site.com) - `Python` - Description ending with a period. [GitHub](https://github.com/owner/repo)
- [Package Name](https://cran.r-project.org/package=pkg) - `R` - Description ending with a period.
- [package-name](https://pypi.org/project/pkg/) - `Python` - Description ending with a period.
```

Rules:

- New non-commercial entries must include one or more concise backtick tags followed by ` - `.
  Tags form a compact tag cloud and are not restricted to programming languages.
- Each tag must use its own backtick pair, for example `` `Python` `C++` `MCP` ``.
- Descriptions must end with a period before the optional `[GitHub](...)` link.
- URLs in new entries must use `https://`.
- A valid GitHub repository used as the main URL or exact `[GitHub](...)` suffix is preferred
  and is a strong positive relevance signal, but it is not universally required. Functional
  section placement requires a repository containing substantive implementation; a thin SDK,
  integration, examples, generated-data, or marketing repository does not qualify.
- Hosted commercial/proprietary products without substantive public source belong in
  `## Commercial & Proprietary Services`, even when a thin repository exists. Repository-less
  services qualify only under the permanent free tier and transparency rules in
  `CONTRIBUTING.md`.
- Treat a commercial service with only a thin SDK, integration, examples, generated-data, or
  marketing repository as repository-less for every eligibility check.
- Backtick tags are optional only for commercial services and other metadata-free
  sections such as `Related Lists`.
- `Historical & Archived Projects` is the documented exception to normal activity and
  archive-state requirements. Entries still require substantive, reachable, documented source
  and the `Historical` tag; use `CONTRIBUTING.md` for eligibility.
- Use `CONTRIBUTING.md` as the user-facing source for contribution rules.

## PR Review Workflow

This repo receives most contributions as pull requests adding README entries.
Use Codex repo skills for repeatable review workflows:

- `$sprr` - single PR reviewer.
- `$bprr` - bulk PR reviewer.
- `$update-pypi-dates` - refresh tracked PyPI last-updated dates.
- `$create-entry` - draft or add README entries from a URL, GitHub issue, or Linear issue.

Review requirements:

1. Only review the PRs the user asked you to review.
2. Use GitHub MCP tools for PR operations, not the `gh` CLI.
3. Present findings before any PR-modifying action.
4. Present exact comment text, label changes, closures and merge targets as one action bundle.
   Obtain one explicit selection before executing that scope; do not request identical consent
   again. Refresh inputs, required checks and duplicates immediately before acting. Material
   changes hold affected actions for renewed review and consent. No automatic public actions.
5. Check section placement, duplicates in `README.md`, entry format, URL format,
   and project activity/documentation. Give substantial positive weight to a verifiable
   GitHub repository mentioned as either the main URL or exact suffix, while confirming that
   functional-section repositories contain substantive implementation.
6. Manually assess commercial entries for free-tier usefulness, payment information,
   public pricing and limits, public documentation/methodology/examples, stable non-tracking
   URLs, concise factual description tone, and repository substance.
7. Commercial submissions without a qualifying permanent free tier—including paid-only,
   trial-only, demo-only, and waitlist-only offerings—are `REJECT`. Reserve `NEEDS CHANGES` for
   correctable evidence or disclosure, wording, URL, documentation, or placement defects when
   the underlying offering can qualify.
8. Use the `reviewed` label only after the user approves a review comment.
   Include the label change in that approved bundle; it is never implied by a verdict.
9. Follow CONTRIBUTING.md's evidence intake and weekly capacity policy: 120 total human PR
   review minutes, including asynchronous decisions and follow-ups; at most four detailed
   candidates, reduced to available time. At most one fully evidenced hosted service replaces
   a slot after source/correction work. No SLA. Implementation and general maintenance have
   separate scheduling; code/infrastructure PR reviews still count toward PR review time.
10. Triage scope, format, duplicates and prior findings before costly investigation. Select new,
    changed or stale submissions; the `reviewed` label is never the sole skip reason. Detect
    body-only changes. Revalidate affected findings, reuse attributable unchanged evidence,
    and summarize waiting/unchanged/pending work. Already-open PRs need only missing evidence;
    no mass re-review or rejection. Route code/infrastructure to code review and preserve
    historical/cleanup paths. Ask one decisive evidence question at uncertainty/timebox limits.
    The README-only checker's rejection of non-README files remains a CI limitation, not a
    project-eligibility verdict; resolve check applicability in code review without waiving gates.
11. Record observed head/base/body and checker provenance. Require both current workflow gates;
    `PR Review` without a trustworthy matching inspected-input stamp is unverified, including
    older green runs. A `pull_request_target` SHA is not the inspected head. Keep eligibility,
    editorial priority and readiness separate; checkable evidence is distinct from claims.
12. Protect small, new, solo and pseudonymous projects; inspect actual implementation and
    dependencies rather than identity or popularity. Preserve the published permanent-free
    rules and CONTRIBUTING.md's meaningful-maintenance, low-change software and educational
    criteria. Classification labels never imply approval.
13. Default-branch committer dates are preliminary screening observations. Old or unknown
    dates require manual evidence assessment; recent dates do not establish meaningful work.
    Record compatibility/stewardship evidence and any exception rationale before approval.
    Archived source remains subject to historical/cleanup rules. Books and papers may use
    reachable authoritative sources; do not require them to manufacture repository activity.

## GitHub MCP Tools

This project expects Codex to have a GitHub MCP server configured for PR work.
Useful tool capabilities include:

- List open pull requests.
- Get PR details, files, comments, labels, and diffs.
- Fetch `README.md` from the default branch for duplicate checks.
- Add PR comments and labels.
- Merge pull requests after explicit user approval.

See `docs/codex-setup.md` for local Codex setup notes. If GitHub MCP tools are
not available in a session, report that PR operations are blocked and ask the
user to configure the MCP server.

## Local Validation Notes

- `scripts/validate_readme.py --diff-from <ref>` is intended for PR checks. It
  validates only added README entries and treats duplicates/URL issues as errors
  for those additions.
- `scripts/validate_readme.py` validates the full README. Legacy format, duplicate, and
  URL problems are reported as warnings unless strict flags are used.
- `parse.py` requires `GITHUB_ACCESS_TOKEN`; `site/generate.py` requires no token.
  Default previews always read README. Explicit CSV mode fails if its input is
  missing. Generated `site/projects.csv` and `site/index.html` are not tracked.
