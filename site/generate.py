#!/usr/bin/env python3
"""Parse README.md and generate a static HTML site for awesome-quant.

Can run in two modes:
1. Default README preview — always reflects the current catalogue.
2. Explicit --source csv — uses enriched data produced by parse.py.
"""

import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.readme_entries import GITHUB_LINK_RE, iter_readme_entries, slugify
from scripts.metadata import FIELDS, checked_at_value, date_value, stars_value


def parse_readme(path: str) -> list[dict]:
    """Adapt the shared catalogue parser to the site's existing entry schema."""
    entries = []
    for entry in iter_readme_entries(path):
        desc = entry.description
        github_match = GITHUB_LINK_RE.search(desc)
        github_url = github_match.group(1) if github_match else entry.github_url
        if github_match:
            desc = GITHUB_LINK_RE.sub("", desc).rstrip(". ").rstrip() + "."
        repo_match = re.match(r"https://github\.com/([\w-]+/[-\w\.]+)", github_url)
        entries.append({
            "project": entry.name,
            "language": entry.languages[0] if entry.languages else "",
            "languages": ",".join(entry.languages),
            "category": entry.section,
            "section_slug": slugify(entry.section),
            "url": entry.url,
            "description": desc,
            "github": bool(github_url),
            "cran": "cran.r-project.org" in entry.url,
            "pypi": "pypi.org" in entry.url or "pypi.python.org" in entry.url,
            "commercial": entry.section == "Commercial & Proprietary Services",
            "github_url": github_url,
            "repo": repo_match.group(1) if repo_match else "",
            "stars": None,
            "last_commit": "",
        })
    return entries


def load_csv(path: str) -> list[dict]:
    """Load projects from CSV produced by parse.py."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize booleans
            for key in ("github", "cran", "pypi", "commercial"):
                row[key] = row.get(key, "").lower() in ("true", "1", "yes")
            # Normalize numbers
            row["stars"] = stars_value(row.get("stars"))
            # Extract github_url and repo from CSV data
            repo = row.get("repo", "")
            row["github_url"] = f"https://github.com/{repo}" if repo else ""
            # Ensure languages column exists
            row["languages"] = row.get("languages", row.get("language", ""))
            # Clean description: strip [GitHub](url) if present
            desc = row.get("description", "")
            desc = re.sub(
                r"\s*\[GitHub\]\(https://github\.com/[\w-]+/[-\w\.]+\)\s*",
                "",
                desc,
            )
            desc = desc.rstrip(". ").rstrip()
            if desc and not desc.endswith("."):
                desc += "."
            row["description"] = desc
            entries.append(row)
    return entries


def format_stars(n: int) -> str:
    """Format star count for display."""
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def metadata_observation(entry: dict, field: str) -> dict:
    """Interpret additive provenance fields; legacy dates have no known meaning."""
    source, label = FIELDS[field]
    value = stars_value(entry.get(field)) if field == "stars" else date_value(entry.get(field))
    checked = checked_at_value(entry.get(field + "_checked_at"))
    attributed = entry.get(field + "_source") == source
    status = entry.get(field + "_status") if checked and attributed else "unknown"
    if status not in ("fresh", "stale"):
        status = "unknown"
    if not attributed and value not in (None, ""):
        label = ("Stars" if field == "stars" else "Date") + " (source unknown)"
    if not attributed or value in (None, ""):
        checked, status = "", "unknown"
    note = {"fresh": "fresh", "stale": "stale (reused)", "unknown": "freshness unknown"}[status]
    note = f"Checked {checked or 'unknown'} · {note}"
    return dict(value=value, label=label, note=note, status=status)


def build_metadata_details(entry: dict) -> str:
    """Expose each field's successful check separately, including on mobile."""
    details = []
    for field, flag in (("last_commit", "github"), ("stars", "github"),
                        ("pypi_upload", "pypi"), ("cran_published", "cran")):
        observation = metadata_observation(entry, field)
        value = observation["value"]
        if not entry.get(flag) and value in (None, ""):
            continue
        display = "Unknown" if value in (None, "") else str(value)
        details.append(
            f'<p><strong>{html.escape(observation["label"])}</strong>: {html.escape(display)} '
            f'<span class="metadata-note">{html.escape(observation["note"])}</span></p>'
        )
    attempted = checked_at_value(entry.get("metadata_attempted_at"))
    if not details:
        return ""
    if attempted:
        details.append(f'<p>Last metadata attempt: {html.escape(attempted)}</p>')
    return '<div class="metadata-details">' + "".join(details) + '</div>'


def build_tags_html(e: dict) -> str:
    """Build tag pills for an entry."""
    esc = html.escape
    tags = []

    # Language tags (from inline backtick tags)
    languages_str = e.get("languages", e.get("language", ""))
    languages = [l.strip() for l in languages_str.split(",") if l.strip()]
    skip_langs = {"Commercial & Proprietary Services", "Related Lists",
                  "Reproducing Works, Training & Books", "Cross-Language Frameworks"}
    for lang in languages:
        if lang and lang not in skip_langs:
            tags.append(
                f'<button class="tag tag-lang" data-filter-type="language" '
                f'data-filter-value="{esc(lang)}">{esc(lang.lower())}</button>'
            )

    # Category tag
    category = e.get("category", "")
    section_slug = e.get("section_slug", "")
    if section_slug:
        tags.append(
            f'<button class="tag tag-section" data-filter-type="category" '
            f'data-filter-value="{esc(category)}">{esc(section_slug)}</button>'
        )

    # Source tags (unchanged)
    if e.get("github"):
        tags.append(
            '<button class="tag tag-source tag-github" '
            'data-filter-type="source" data-filter-value="github">github</button>'
        )
    if e.get("cran"):
        tags.append(
            '<button class="tag tag-source tag-cran" '
            'data-filter-type="source" data-filter-value="cran">cran</button>'
        )
    if e.get("pypi"):
        tags.append(
            '<button class="tag tag-source tag-pypi" '
            'data-filter-type="source" data-filter-value="pypi">pypi</button>'
        )
    if e.get("commercial"):
        tags.append(
            '<button class="tag tag-source tag-commercial" '
            'data-filter-type="source" data-filter-value="commercial">commercial</button>'
        )

    return "\n          ".join(tags)


def build_tag_cloud(entries: list[dict]) -> str:
    """Build a tag cloud of popular languages and categories."""
    from collections import Counter

    # Count language frequencies
    lang_counts = Counter()
    for e in entries:
        langs = [l.strip() for l in e.get("languages", e.get("language", "")).split(",") if l.strip()]
        lang_counts.update(langs)

    # Remove non-language sections
    skip = {"Commercial & Proprietary Services", "Related Lists", "Reproducing Works, Training & Books", "Cross-Language Frameworks"}
    for s in skip:
        lang_counts.pop(s, None)

    # Count category frequencies
    cat_counts = Counter(e.get("category", "") for e in entries if e.get("category"))

    # Get top items
    top_langs = lang_counts.most_common(8)  # Top 8 languages
    top_cats = cat_counts.most_common(6)    # Top 6 categories

    if not top_langs and not top_cats:
        return ""

    # Combine and sort by frequency
    all_items = []
    for lang, count in top_langs:
        all_items.append(("language", lang, count))
    for cat, count in top_cats:
        all_items.append(("category", cat, count))

    # Sort by count descending
    all_items.sort(key=lambda x: x[2], reverse=True)

    # Calculate size scale (1.0 to 1.6x)
    min_count = min(item[2] for item in all_items)
    max_count = max(item[2] for item in all_items)
    count_range = max_count - min_count if max_count > min_count else 1

    tags = []
    esc = html.escape
    for tag_type, value, count in all_items:
        # Calculate font size: 1.0 to 1.6
        size = 1.0 + ((count - min_count) / count_range * 0.6)

        if tag_type == "language":
            tags.append(
                f'<button class="tag tag-lang tag-cloud-item" '
                f'data-filter-type="language" data-filter-value="{esc(value)}" '
                f'style="font-size: {size:.2f}em;">{esc(value.lower())}</button>'
            )
        else:  # category
            tags.append(
                f'<button class="tag tag-section tag-cloud-item" '
                f'data-filter-type="category" data-filter-value="{esc(value)}" '
                f'style="font-size: {size:.2f}em;">{esc(value)}</button>'
            )

    return f"""        <div class="tag-cloud">
          <div class="tag-cloud-label">Popular filters:</div>
          <div class="tag-cloud-items">
            {chr(10).join("            " + tag for tag in tags)}
          </div>
        </div>"""


def generate_html(entries: list[dict]) -> str:
    """Generate the full HTML page from project entries."""
    languages = sorted(
        set(
            lang.strip()
            for e in entries
            for lang in e.get("languages", e.get("language", "")).split(",")
            if lang.strip()
            and lang.strip() not in {
                "Commercial & Proprietary Services",
                "Related Lists",
                "Reproducing Works, Training & Books",
                "Cross-Language Frameworks",
            }
        )
    )

    # Generate tag cloud
    tag_cloud_html = build_tag_cloud(entries)

    # Build table rows
    rows = []
    for i, e in enumerate(entries, 1):
        esc = html.escape
        name = esc(e["project"])
        url = esc(e["url"])
        desc = esc(e["description"])
        category = esc(e.get("category", ""))
        github_url = esc(e.get("github_url", ""))
        stars_observation = metadata_observation(e, "stars")
        stars = stars_observation["value"]
        dates = [(metadata_observation(e, field), e.get(flag)) for field, flag in
                 (("last_commit", "github"), ("pypi_upload", "pypi"), ("cran_published", "cran"))]
        update = next((observation for observation, _ in dates if observation["value"]),
                      next((observation for observation, applies in dates if applies), dates[0][0]))
        update_date = update["value"] or ""
        is_github = e.get("github", False)
        is_cran = e.get("cran", False)
        is_pypi = e.get("pypi", False)
        is_commercial = e.get("commercial", False)

        # Exact tag strings, including spaces and HTML-sensitive characters.
        tags_attr = esc(json.dumps([
            l.strip() for l in e.get("languages", e.get("language", "")).split(",") if l.strip()
        ]))

        # Stars display
        stars_html = (
            f'<span class="stars" title="{stars:,} stars; {esc(stars_observation["note"])}">'
            f'<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
            f" {format_stars(stars)}</span>"
            if stars is not None
            else '<span class="metadata-unknown">Unknown</span>'
        )
        if stars is not None and stars_observation["status"] != "fresh":
            stars_html += f'<span class="metadata-label">{esc("stale (reused)" if stars_observation["status"] == "stale" else "source / check date unknown")}</span>'

        # A registry date never acquires the label or provenance of a commit.
        last_update_html = (
            f'<span class="last-update" title="{esc(update["note"])}">{esc(update_date) or "Unknown"}</span>'
            f'<span class="metadata-label">{esc(update["label"]) if update_date or any(applies for _, applies in dates) else "No date available"}</span>'
        )
        if update_date and update["status"] == "stale":
            last_update_html += '<span class="metadata-label">stale (reused)</span>'
        metadata_details = build_metadata_details(e)

        # Source flags for data attributes
        sources = []
        if is_github:
            sources.append("github")
        if is_cran:
            sources.append("cran")
        if is_pypi:
            sources.append("pypi")
        if is_commercial:
            sources.append("commercial")
        sources_attr = esc(" ".join(sources))

        tags_html = build_tags_html(e)

        rows.append(
            f"""      <tr class="row" data-tags="{tags_attr}" data-category="{category}" data-sources="{sources_attr}" data-stars="{stars if stars is not None else -1}" data-update="{esc(update_date)}">
        <td class="col-num">{i}</td>
        <td class="col-name">
          <a href="{url}" target="_blank" rel="noopener">{name}</a>
          <span class="mobile-category">{category}</span>
        </td>
        <td class="col-stars">{stars_html}</td>
        <td class="col-update">{last_update_html}</td>
        <td class="col-tags">
          {tags_html}
        </td>
        <td class="col-arrow"><span class="arrow">&#8250;</span></td>
      </tr>
      <tr class="expand-row" hidden>
        <td colspan="6">
          <div class="expand-content">
            <p class="expand-desc">{desc}</p>
            {metadata_details}
            <div class="expand-links">
              <a href="{url}" target="_blank" rel="noopener">{url}</a>
              {f'<a href="{github_url}" target="_blank" rel="noopener">{github_url}</a>' if github_url and github_url != url else ''}
            </div>
          </div>
        </td>
      </tr>"""
        )

    total = len(entries)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awesome Quant</title>
  <meta name="description" content="A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance).">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="static/style.css">
</head>
<body>
  <a href="#content" class="sr-only">Skip to content</a>

  <header class="hero">
    <div class="hero-inner">
      <nav class="nav">
        <span class="nav-brand">awesome-quant</span>
        <div class="nav-links">
          <a href="https://github.com/wilsonfreitas/awesome-quant/blob/main/CONTRIBUTING.md" class="nav-submit">Submit a Project</a>
          <a href="https://github.com/wilsonfreitas/awesome-quant/blob/main/docs/choosing-backtesting.md">Choosing a backtester</a>
          <a href="https://github.com/wilsonfreitas/awesome-quant">GitHub</a>
          <button class="theme-toggle" aria-label="Toggle dark mode" title="Toggle dark mode">
            <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
            <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          </button>
        </div>
      </nav>
      <div class="hero-content">
        <h1>Awesome Quant</h1>
        <p class="hero-subtitle">A curated list of insanely awesome libraries, packages and resources for Quants.</p>
        <p class="hero-maintained">Maintained by <a href="https://github.com/wilsonfreitas">Wilson Freitas</a></p>
        <div class="hero-stats">
          <span class="stat"><strong>{total}</strong> projects</span>
          <span class="stat-sep"></span>
          <span class="stat"><strong>{len(languages)}</strong> tags</span>
        </div>
        <a href="#content" class="hero-cta">Browse the List</a>
      </div>
    </div>
  </header>

  <main id="content">
    <section class="list-section">
      <div class="shell">
        <div class="controls">
          <div class="search-wrap">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input type="search" id="search" class="search-input" placeholder="Search projects..." autocomplete="off" aria-label="Search projects">
            <kbd class="search-kbd">/</kbd>
          </div>
        </div>

{tag_cloud_html}

        <div class="filter-bar" id="filter-bar" style="display:none">
          <span class="filter-label">Filtered by:</span>
          <span class="filter-value" id="filter-value"></span>
          <button class="filter-clear" id="filter-clear">Clear filter</button>
        </div>

        <div class="table-wrap">
          <table class="table" id="project-table">
            <thead>
              <tr>
                <th class="col-num">#</th>
                <th class="col-name" data-sort="name">Project <span class="sort-arrow"></span></th>
                <th class="col-stars" data-sort="stars">Stars <span class="sort-arrow"></span></th>
                <th class="col-update" data-sort="update">Last Update <span class="sort-arrow"></span></th>
                <th class="col-tags">Tags</th>
                <th class="col-arrow"></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>

        <div class="no-results" id="no-results" hidden>
          <p>No projects match your search.</p>
        </div>

        <div class="results-count" id="results-count"></div>
      </div>
    </section>

    <section class="cta-section">
      <div class="shell">
        <h2>Know a great project?</h2>
        <p>Contribute to the list by opening a pull request on GitHub.</p>
        <a href="https://github.com/wilsonfreitas/awesome-quant" class="btn" target="_blank" rel="noopener">Contribute on GitHub</a>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="shell">
      <span>Maintained by <a href="https://github.com/wilsonfreitas">Wilson Freitas</a></span>
      <span class="footer-sep">&middot;</span>
      <a href="https://github.com/wilsonfreitas/awesome-quant">GitHub</a>
      <span class="footer-sep">&middot;</span>
      <a href="https://awesome.re">awesome.re</a>
    </div>
  </footer>

  <script src="static/main.js"></script>
</body>
</html>"""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("readme", "csv"), default="readme")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--csv", type=Path, default=ROOT / "site/projects.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "site/index.html")
    args = parser.parse_args(argv)
    source = args.csv if args.source == "csv" else args.readme
    try:
        entries = load_csv(source) if args.source == "csv" else parse_readme(source)
        args.output.write_text(generate_html(entries), encoding="utf-8")
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR generating site from {source}: {exc}", file=sys.stderr)
        return 1
    print(f"Loaded {len(entries)} projects from {source}")
    print(f"Generated {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
