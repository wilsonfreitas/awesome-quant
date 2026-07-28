---
name: preflight
description: Preflight health check for awesome-quant — curated quant list + scraper scripts (uv). Use before starting a session in this project, when the user runs /preflight, or asks whether the project is healthy/ready.
---

# Preflight — awesome-quant

Project root: `/Users/josh/IntelustryProjects/active/awesome-quant`

Run each check, record PASS / FAIL / WARN, then print the status table.

## Checks

**[1] Python env for scrapers**
```bash
cd /Users/josh/IntelustryProjects/active/awesome-quant && uv run python -c "print('PASS uv env ok')" 2>&1 | tail -1
```

**[2] Repo state**
```bash
cd /Users/josh/IntelustryProjects/active/awesome-quant && git status --short | head -5
```


## Status Table

After all checks, print a summary:

```
PREFLIGHT — AWESOME-QUANT
┌──────────────────────────┬────────┬──────────────────────────┐
│ Check                    │ Status │ Note                     │
├──────────────────────────┼────────┼──────────────────────────┤
│ ...                      │  ...   │ ...                      │
└──────────────────────────┴────────┴──────────────────────────┘
Overall: READY / DEGRADED / BLOCKED
```

- **READY** — all checks pass
- **DEGRADED** — non-critical failures (optional service down, missing dev deps)
- **BLOCKED** — a critical dependency is down (required env, API key, services needed to run)

If BLOCKED, list the exact fix commands before proceeding.

**BLOCKED when:** never — mostly a docs repo; only the scraper scripts need the env.
