"""
Index Doxygen API pages into the same Algolia index used by the website.

This script fetches the preCICE Participant class Doxygen page,
extracts indexable nodes, and pushes them to the same Algolia index
used by the website.

Usage:
  python scripts/index_doxygen.py              # push to Algolia
  python scripts/index_doxygen.py --dry-run    # print records, don't push

Requires: ALGOLIA_API_KEY environment variable (unless --dry-run).
Depends: beautifulsoup4, requests, algoliasearch>=4.0
"""

import hashlib
import json
import os
import sys

import requests
from bs4 import BeautifulSoup

ALGOLIA_APP_ID = "LIT6P0EW26"
ALGOLIA_INDEX_NAME = "jekyll"
SOURCE_TAG = "api-docs"
MAX_HTML_SIZE = 5000

# Pages to index: (url, friendly_title_override)
# Add more Doxygen pages here as needed.
PAGES = [
    "https://api.precice.org/cpp/latest/classprecice_1_1Participant.html",
]


def fetch_page(url):
    """Fetch a URL and return a BeautifulSoup object."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def extract_records(soup, url):
    """
    Extract Algolia records from a Doxygen page.

    Splits content by indexable nodes (p, code, table). Each record
    includes the nearest heading for context.

    Skips nodes nested inside other indexable nodes to avoid
    duplicates, deduplicates by objectID, and skips oversized nodes.
    """
    title = soup.find("title")
    page_title = title.get_text(strip=True) if title else "preCICE API"

    indexable_tags = {"p", "code", "table"}
    seen_ids = set()
    records = []

    for node in soup.find_all(["p", "code", "table"]):
        content = node.get_text(strip=True)
        if not content or len(content) < 20:
            continue

        # Skip nodes nested inside another indexable node
        # (e.g. <code> inside <p>) to avoid duplicate content
        if any(parent.name in indexable_tags for parent in node.parents):
            continue

        html_str = str(node)
        if len(html_str) > MAX_HTML_SIZE:
            continue

        # Find nearest preceding heading for context
        heading = ""
        anchor = ""
        for prev in node.find_all_previous(["h1", "h2", "h3", "h4"]):
            heading = prev.get_text(strip=True)
            anchor = prev.get("id", "")
            break

        # Stable objectID: hash of url + anchor + content prefix
        object_id = hashlib.md5(
            f"{url}#{anchor}#{content[:100]}".encode()
        ).hexdigest()

        # Deduplicate
        if object_id in seen_ids:
            continue
        seen_ids.add(object_id)

        records.append(
            {
                "objectID": object_id,
                "html": html_str,
                "content": content,
                "headings": [heading] if heading else [],
                "anchor": anchor,
                "title": page_title,
                "permalink": url,
                "url": url,
                "type": "page",
                "source": SOURCE_TAG,
                "language": "cpp",
            }
        )

    return records


def push_to_algolia(records, api_key):
    """Replace API docs records in Algolia with fresh records."""
    from algoliasearch.search.client import SearchClientSync
    from algoliasearch.search.models.delete_by_params import DeleteByParams

    client = SearchClientSync(ALGOLIA_APP_ID, api_key)

    print("  Deleting stale api-docs records...")
    response = client.delete_by(
        index_name=ALGOLIA_INDEX_NAME,
        delete_by_params=DeleteByParams(filters=f"source:{SOURCE_TAG}"),
    )
    client.wait_for_task(index_name=ALGOLIA_INDEX_NAME, task_id=response.task_id)
    print("  Deletion complete.")

    client.save_objects(
        index_name=ALGOLIA_INDEX_NAME,
        objects=records,
    )


def main():
    dry_run = "--dry-run" in sys.argv

    if not dry_run:
        api_key = os.environ.get("ALGOLIA_API_KEY")
        if not api_key:
            print("Error: ALGOLIA_API_KEY environment variable is required.")
            sys.exit(1)

    total_records = 0

    for url in PAGES:
        print(f"Fetching {url} ...")
        soup = fetch_page(url)
        records = extract_records(soup, url)
        print(f"  Extracted {len(records)} records")

        if dry_run:
            preview = list(records[:3])
            print(json.dumps(preview, indent=2))
            print(f"  ... ({len(records)} total, showing first 3)")
        else:
            if not records:
                print("Error: No records extracted, refusing to wipe existing api-docs index entries.")
                sys.exit(1)
            push_to_algolia(records, api_key)
            print(f"  Pushed {len(records)} records to Algolia")

        total_records += len(records)

    print(f"Done. Total records indexed: {total_records}")


if __name__ == "__main__":
    main()
