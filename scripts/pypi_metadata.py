"""Shared PyPI distribution-upload metadata, independent of version ordering."""

from datetime import datetime, timezone
import json
import sys
from urllib.parse import quote
from urllib.request import urlopen


def latest_upload_date(payload: dict) -> str | None:
    """Return the latest valid upload date in UTC across all distribution files."""
    releases = payload.get('releases', {})
    if not isinstance(releases, dict):
        return None
    latest = None
    for files in releases.values():
        if not isinstance(files, list):
            continue
        for file in files:
            timestamp = file.get('upload_time_iso_8601') if isinstance(file, dict) else None
            if not isinstance(timestamp, str):
                continue
            try:
                uploaded = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if uploaded.tzinfo is None:
                    uploaded = uploaded.replace(tzinfo=timezone.utc)
                uploaded = uploaded.astimezone(timezone.utc)
            except (ValueError, OverflowError):
                continue
            if latest is None or uploaded > latest:
                latest = uploaded
    return latest.date().isoformat() if latest else None


def get_pypi_last_updated(package_name: str) -> str | None:
    """Fetch metadata without changing caller files; unavailable dates are None."""
    try:
        url = f'https://pypi.org/pypi/{quote(package_name, safe="")}/json'
        with urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode('utf-8'))
        return latest_upload_date(payload) if isinstance(payload, dict) else None
    except (OSError, ValueError) as exc:
        print(f'PyPI metadata unavailable for {package_name}: {type(exc).__name__}', file=sys.stderr)
        return None
