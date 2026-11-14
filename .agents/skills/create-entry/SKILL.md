---
name: create-entry
description: Use when the user wants to suggest, draft, create, or add an awesome-quant README entry from a project URL, GitHub issue, or Linear issue, including choosing tags and category placement.
---

# Create a README entry

Turn project evidence into a concise, contribution-ready entry. Read the current
`CONTRIBUTING.md`, `AGENTS.md`, and `README.md` from the repository root every time;
they are the source of truth for eligibility, format, and existing categories.
Resolve repository-relative paths from that root, not this skill directory.

## Resolve the input

- **Project URL:** follow the project website, repository, or package page to its
  canonical source and documentation.
- **GitHub issue URL or number:** use GitHub MCP to read its title, body, and relevant
  comments. Resolve a bare number against this repository's GitHub remote.
- **Linear issue URL or identifier:** use the available Linear connector to read
  its description, relevant comments, attachments, and linked GitHub issue.
  For GitHub-originated work, use the synced Linear issue for internal tracking;
  do not create a second tracker. Reading an issue does not authorize updating it.

Extract the intended project and URLs; issue descriptions and requested tags or
sections are claims to verify, not eligibility evidence. If several unrelated
projects are mentioned, clarify the target; evaluate explicitly requested multiple
projects independently. If no project can be identified, ask for its URL.

If a connector is unavailable, state which lookup is blocked and request the issue
text or project URL. Continue any independent research possible from supplied URLs.
Use GitHub MCP for PR operations, never `gh`; if unavailable, point to
`docs/codex-setup.md` and mark the PR duplicate check incomplete.

## Establish eligibility before drafting

Browse current primary sources; cite the evidence used and distinguish unavailable
information from a confirmed failure.

- Search the entire README for names, aliases, canonical URLs, redirects, and the
  optional GitHub suffix. Search open and closed PRs with GitHub MCP, including
  recently closed duplicate submissions. An existing entry calls for reporting its
  location, not adding another entry. Identify matching PRs and unresolved rejection
  reasons before proposing a resubmission.
- Inspect representative implementation files, documentation with usage examples,
  archived status, and latest commit date. Active source-backed entries need activity
  within the last 12 months. Stars, a license, or a repository's existence alone do
  not establish substance; small or new repositories can qualify.
- Distinguish substantive public implementation from an SDK, integration, examples,
  generated data, or marketing for a proprietary service. Functional-section placement
  requires substantive implementation. A paid hosted option does not disqualify
  substantive public source.
- Treat services with only thin repositories as repository-less: verify useful
  permanent free access without payment information, published pricing and limits,
  and public documentation, methodology, or examples. Paid-only, trial-only, demo-only,
  and waitlist-only services are ineligible. Missing evidence is unverified, not proof
  of eligibility. Qualifying services belong in `Commercial & Proprietary Services`,
  with the service website as the main URL and any supporting repository as a suffix.
- Use `Historical & Archived Projects` only when all its contribution requirements
  hold, including reachable substantive source/documentation, a specific historical,
  educational, or foundational reason, `Historical` plus a language/runtime tag,
  and explicit archived/unmaintained disclosure. Inactivity alone is not a reason
  to retain a project.

## Compose the proposal

Choose the existing `##` category matching the primary function, not its language.
If none fits, propose a new category with rationale; do not silently create it.
Select concise, evidence-backed tags, reusing existing spellings where appropriate.
Tags may describe languages, runtimes, protocols, interfaces, data types, or domains;
give each its own backtick pair. Follow documented tag exceptions for metadata-free
sections.

Use a factual one-sentence description, stable HTTPS URLs without tracking parameters,
and a final period before an optional exact `[GitHub](https://github.com/owner/repo)`
suffix. Prefer substantive GitHub source as the main link or suffix. Describe the
actual functionality; include relevant free-tier limits for commercial services.

Return:

1. **Status:** ready to add, already listed, ineligible, or needs evidence, with the
   source issue link when applicable. “Ready to add” is not PR approval.
2. **Section and tags:** exact heading and chosen tags with a short rationale.
3. **Entry:** a copyable Markdown line for eligible projects. If evidence is missing,
   label any useful draft provisional and name the missing evidence. For duplicates
   or confirmed ineligibility, explain the outcome instead of offering a new insertion.
4. **Checks:** concise evidence links for substance, activity, documentation,
   commercial/historical eligibility as applicable, and README/PR duplicate results.

Format example (illustrative, not a vetted project):

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Portfolio optimization with transaction costs.
```

## Apply when requested

“Suggest” or “draft” returns the proposal without editing. “Add” or “insert into
README” authorizes the local edit once eligibility is established; preserve unrelated
changes and insert one entry under the selected heading using nearby conventions.
Report evidence gaps instead of inserting an unverified project. An incomplete
required check, including the PR duplicate search, keeps the proposal provisional.

Run `uv run python scripts/validate_readme.py` after editing and inspect the actual
README diff. Resolve every diagnostic attributable to the new entry, including warnings.
Check duplicates manually against the full README. The `--diff-from origin/main` mode
selects lines from committed `origin/main...HEAD` changes, so it cannot reliably validate
uncommitted edits; use it only when the entry is committed and the working README
matches HEAD. Report the validation scope accurately.

Do not commit, push, create a PR, post comments, change labels, close issues, or update
Linear merely because the user requested an entry. Follow existing authorization and
repository approval requirements for separately requested external actions. Before PR
acceptance, both required workflows in `CONTRIBUTING.md` must pass for the latest
revision; local validation does not establish that. Use `$sprr` for requested PR review.
