# Catalogue metadata

`README.md` defines catalogue membership, tags, descriptions, and placement.
Metadata is an observation of a source, not an editorial review or a guarantee
that a project works. A recent package upload does not demonstrate recent
repository development.

## Dates and counts

`parse.py` writes `site/projects.csv`. Its observation fields have distinct meanings:

| CSV field | Source identifier | Meaning |
| --- | --- | --- |
| `last_commit` | `github_commit` | UTC calendar date of the default branch head commit's **committer** timestamp from GitHub. This is neither author time nor repository `pushed_at`. |
| `stars` | `github` | GitHub repository stargazer count, including an observed zero. |
| `pypi_upload` | `pypi_upload` | Latest valid distribution upload date across all PyPI releases, using the shared PyPI helper. |
| `cran_published` | `cran_publication` | Publication date reported on the CRAN package page. |

Each field also has additive `_source`, `_checked_at`, and `_status` columns.
For example, `stars_checked_at` is the timezone-qualified UTC timestamp of the
last **successful** star-count observation, independent of `last_commit_checked_at`.
Dates are `YYYY-MM-DD`. Empty values mean unknown; an unavailable star count is
empty, never an invented zero.

`metadata_attempted_at` records this build's attempt. It does not advance any
field's successful-check timestamp. Registry dates are fetched independently of
GitHub and never stored in `last_commit`.

## Freshness and failed requests

- `fresh`: the field was successfully observed in this build. This describes the
  observation, not how recent the commit, publication, or upload was.
- `stale`: this build could not observe the field, so it reused its last successful
  value, source, and check timestamp. Repeated failures keep that original check.
- `unknown`: no verifiable successful observation is available for this identity.
  Source and check timestamp are empty.

A commit request can fail while stars succeed, or GitHub can fail while PyPI
succeeds. Only successful fields advance. Timeouts, missing commits, malformed
dates, invalid counts, and unavailable sources do not replace successful history.
GitHub requests use a ten-second timeout without retries; registry HTTP requests
also use ten-second timeouts. A malformed or absent date is unknown, not today's
date. Check timestamps remain visible so readers can judge the age of observations
between deployments; there is no automatic age-based freshness threshold.

The site displays a GitHub commit date when available, otherwise a PyPI upload or
CRAN publication date, with its source label. Expanding an entry shows applicable
fields' values, successful-check timestamps, and freshness, including on mobile.
GitHub entries show commits and stars, PyPI entries show uploads, and CRAN entries
show publications. Actual legacy values remain visible regardless of source flags.
Reused values are marked **stale (reused)**. Date sorting uses the displayed date,
not the freshness timestamp or source label; dates from different sources have
different meanings. Unknown star counts sort below observed zero in descending
star order.

## Identity and compatibility

`metadata_identity` is a JSON array of the README project name, exact primary URL,
declared GitHub repository, and effective repository. A matching identity is
required before observations may be reused. Changing a name, primary URL, or
declared/discovered repository invalidates the old observations. Description,
tag, and category edits do not invalidate observations of the same project.

When CRAN previously supplied the repository, a failed discovery can reuse that
repository for the unchanged entry. A successful package page that removes or
changes its repository link invalidates the previous observations. A response
without a complete, valid CRAN publication-date cell and properly ordered opening
and closing `html`/`body` tags is treated as unavailable, not as evidence of
repository removal. This includes truncation after the publication date but
before later repository links. Only observations with the expected source, a valid
value, and a valid successful-check timestamp can be reused. Trailing slashes in
GitHub repository URLs are normalized for repository lookup; the identity still
retains the exact primary URL and never carries observations to another repository.

Older CSV columns remain supported by the site. A legacy `last_commit` may have
been a registry date, so it is shown as **Date (source unknown)**. Legacy
values have unknown freshness; missing provenance is never inferred from source
flags. Legacy CSV observations are not reused by the parser because their
identity and observation semantics cannot be verified.

## Builds and persistence

Default `uv run python site/generate.py` previews always parse the current README,
without tokens, enrichment, or cached metadata. Production explicitly runs
`uv run python site/generate.py --source csv` after the parser. CSV mode fails if
its input is absent; it does not silently switch to README mode.

Before production enrichment, `.github/workflows/build.yml` reads only
`projects.csv` from this repository's `gh-pages` branch using the authenticated
checkout's `origin`. It fetches Git objects and copies that file; it does not
check out or execute published content, or consume pull-request artifacts.
The enriched CSV is deployed alongside the site and restored by the next clean
build. No separate cache service or expiry policy is required.

A missing branch or missing CSV permits the first build with unknown values for
failed lookups. A failed tree listing, corrupt Git object, or transport failure
restoring an existing publication stops the build before deployment, protecting
the published history. Locally the parser reads its existing destination CSV
before enrichment and replaces it atomically
afterward. The CSV is generated data and stays untracked. An absent, unreadable,
or legacy local cache degrades to unknown fields when enrichment fails.
