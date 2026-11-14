"""Shared CSV observation semantics; no network access or enrichment dependencies."""

from datetime import datetime, timezone
import re


FIELDS = {
    "last_commit": ("github_commit", "GitHub commit"),
    "stars": ("github", "GitHub stars"),
    "pypi_upload": ("pypi_upload", "PyPI upload"),
    "cran_published": ("cran_publication", "CRAN publication"),
}


def date_value(value):
    """Validate calendar dates, converting timestamps to a UTC calendar date."""
    if isinstance(value, datetime):
        timestamp = value
    elif isinstance(value, str):
        try:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
            if "T" not in value:
                return ""
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, OverflowError):
            return ""
    else:
        return ""
    try:
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc).date().isoformat()
    except (ValueError, OverflowError):
        return ""


def checked_at_value(value):
    """A successful observation needs a timezone-qualified timestamp."""
    if not isinstance(value, str) or "T" not in value:
        return ""
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return timestamp.astimezone(timezone.utc).isoformat() if timestamp.tzinfo else ""
    except (ValueError, OverflowError):
        return ""


def stars_value(value):
    """Blank, invalid, and negative counts are unknown; observed zero is valid."""
    if isinstance(value, bool):
        return None
    # Older pandas CSVs serialized integral counts with a .0 suffix.
    if not re.fullmatch(r"\d+(?:\.0+)?", str(value)):
        return None
    return int(str(value).split(".")[0])
