"""Thin Sharadar (Nasdaq Data Link) datatable client with on-disk caching.

Access requires two things this environment may not have yet:
  1. env var NASDAQ_DATA_LINK_API_KEY
  2. network egress to data.nasdaq.com
Both absent -> a clear RuntimeError, never fabricated data (spec §2.3:
failed sources are logged, never silently substituted).
"""

import hashlib
import io
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

API = "https://data.nasdaq.com/api/v3/datatables/SHARADAR/{table}.csv"
CACHE = Path(__file__).parent / "cache"

ENABLE_HELP = (
    "Sharadar access is not configured. Two steps:\n"
    "  1. Add env var NASDAQ_DATA_LINK_API_KEY in the Claude Code environment settings\n"
    "  2. Allow data.nasdaq.com in the environment's network policy\n"
    "See backtest/README.md."
)


def _key() -> str:
    key = os.environ.get("NASDAQ_DATA_LINK_API_KEY", "").strip()
    if not key:
        raise RuntimeError(ENABLE_HELP)
    return key


def fetch(table: str, use_cache: bool = True, **filters) -> pd.DataFrame:
    """Fetch a full SHARADAR datatable slice, following pagination cursors.

    filters are passed through as query params, e.g.
      fetch("SF1", dimension="ARQ", ticker="AAPL")
      fetch("SEP", **{"date.gte": "2010-01-01"})
    """
    cache_id = hashlib.sha256(
        json.dumps([table, sorted(filters.items())]).encode()
    ).hexdigest()[:16]
    cache_file = CACHE / f"{table}-{cache_id}.csv.gz"
    if use_cache and cache_file.exists():
        return pd.read_csv(cache_file)

    key = _key()
    frames = []
    cursor = None
    while True:
        params = dict(filters, api_key=key, **{"qopts.export": "false"})
        if cursor:
            params["qopts.cursor_id"] = cursor
        url = API.format(table=table) + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "investment-os-backtest"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                cursor = resp.headers.get("Cursor_ID") or None
                frames.append(pd.read_csv(io.BytesIO(resp.read())))
        except Exception as e:  # noqa: BLE001 - report, never substitute
            raise RuntimeError(f"Sharadar fetch failed for {table}: {e}\n{ENABLE_HELP}") from e
        if not cursor:
            break

    df = pd.concat(frames, ignore_index=True)
    CACHE.mkdir(exist_ok=True)
    df.to_csv(cache_file, index=False, compression="gzip")
    return df
