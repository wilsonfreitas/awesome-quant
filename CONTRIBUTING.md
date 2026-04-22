# Contributing

Your contributions are always welcome! Please ensure your pull request meets the following guidelines.

## Entry Format

Each entry must include one or more language tags and follow one of these formats:

### Single language

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` - Short description ending with a period.
```

### Multiple languages

For projects available in multiple languages, list them as backtick-delimited tags:

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Short description ending with a period.
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
- GitHub repository URLs are strongly preferred. Projects with GitHub repos get automated tracking of stars, activity, and archive status on [awesome-quant.com](https://awesome-quant.com/).
- The description must end with a period (before the `[GitHub]` link, if present).
- Keep descriptions concise — one sentence.

## Quality Requirements

- **Active**: Project must show recent activity (commits within the last 12 months).
- **Documented**: Clear README with usage examples.


## Commercial & Proprietary Projects

Commercial and proprietary projects are welcome. They will be placed under the **Commercial & Proprietary Services** section. Include a link to the product website and a brief description of what it offers.

**Placement rule:** If the main URL (the first link) is a commercial website and there is no GitHub repository link (as a second URL), the entry **must** be placed in the **Commercial & Proprietary Services** section. This applies to:
- SaaS platforms and APIs
- Commercial data providers
- Paid subscription services
- Any proprietary product without open-source code

Projects with GitHub repositories may be placed in other sections based on their functionality.

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

## Before Submitting

1. Search the existing list to make sure the project is not already included.
2. Search previous Pull Requests (open and closed) to avoid duplicates.
3. Make sure the entry format matches exactly — our parser relies on it.

## Automatic Rejection

PRs will be closed if:

- Multiple projects added in a single PR.
- Entry format does not match the required pattern.
- Duplicate of an existing entry or a recently closed PR.
- Project is archived or abandoned.
- Empty PR description.
