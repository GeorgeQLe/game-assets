#!/usr/bin/env python3
"""Audit Kenney's RSS feed against the central game-assets catalog."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


DEFAULT_FEED_URL = "https://kenney.nl/feed"


@dataclass
class FeedEntry:
    title: str
    slug: str
    published: str
    category: str
    url: str
    status: str = "unclassified"
    repositories: list[str] | None = None


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Kenney's official RSS feed with game-assets/repos.json."
    )
    parser.add_argument("--repo-root", type=Path, default=repository_root())
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--feed-url", default=DEFAULT_FEED_URL)
    source.add_argument("--feed-file", type=Path)
    parser.add_argument(
        "--skip-github",
        action="store_true",
        help="Report newer feed entries without searching indexed manifests.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser.parse_args()


def load_feed(args: argparse.Namespace) -> bytes:
    if args.feed_file:
        return args.feed_file.read_bytes()
    request = urllib.request.Request(
        args.feed_url,
        headers={"User-Agent": "GeorgeQLe-game-assets-refresh/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def required_text(node: ET.Element, tag: str) -> str:
    value = node.findtext(tag)
    if not value or not value.strip():
        raise ValueError(f"RSS item is missing {tag}")
    return value.strip()


def parse_feed(payload: bytes) -> tuple[str, list[FeedEntry]]:
    root = ET.fromstring(payload)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS feed is missing channel")

    build_date = parsedate_to_datetime(required_text(channel, "lastBuildDate")).date()
    entries: list[FeedEntry] = []
    for item in channel.findall("item"):
        published = parsedate_to_datetime(required_text(item, "pubDate")).date()
        url = required_text(item, "link")
        slug = (item.findtext("guid") or urlparse(url).path.rstrip("/").split("/")[-1]).strip()
        entries.append(
            FeedEntry(
                title=required_text(item, "title"),
                slug=slug,
                published=published.isoformat(),
                category=(item.findtext("category") or "").strip(),
                url=url,
                repositories=[],
            )
        )
    return build_date.isoformat(), entries


def github_manifest(owner: str, repo: str) -> dict[str, Any] | list[Any]:
    command = [
        "gh",
        "api",
        f"repos/{owner}/{repo}/contents/manifest.json",
        "-H",
        "Accept: application/vnd.github.raw+json",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def repo_owner(repo: dict[str, Any]) -> str:
    path = urlparse(repo["url"]).path.strip("/").split("/")
    if len(path) != 2:
        raise ValueError(f"Unsupported repository URL: {repo['url']}")
    return path[0]


def kenney_asset_slug(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    if parsed.netloc.lower() not in {"kenney.nl", "www.kenney.nl"}:
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) != 2 or parts[0] != "assets":
        return None
    return parts[1]


def matching_repositories(
    entries: list[FeedEntry], repos: list[dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    for repo in repos:
        try:
            manifest = github_manifest(repo_owner(repo), repo["name"])
        except (
            OSError,
            subprocess.CalledProcessError,
            json.JSONDecodeError,
            ValueError,
        ) as error:
            errors.append(f"{repo['name']}: {error}")
            continue

        if isinstance(manifest, dict):
            assets = manifest.get("assets", [])
        elif isinstance(manifest, list):
            assets = manifest
        else:
            errors.append(f"{repo['name']}: unsupported manifest root")
            continue

        source_slugs = {
            kenney_asset_slug(asset.get("sourceUrl"))
            for asset in assets
            if isinstance(asset, dict)
        }
        for entry in entries:
            if entry.slug in source_slugs:
                entry.repositories.append(repo["name"])
    return errors


def render_text(result: dict[str, Any]) -> None:
    print(f"Kenney feed through: {result['feedThrough']}")
    print(f"Catalog through:     {result['catalogThrough']}")
    print(f"Status:              {result['status'].upper()}")
    for entry in result["candidates"]:
        repos = ", ".join(entry["repositories"]) or "not found"
        print(
            f"{entry['status'].upper():9} {entry['published']}  "
            f"{entry['title']} ({entry['slug']}) -> {repos}"
        )
    for error in result["errors"]:
        print(f"ERROR  {error}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    catalog_path = args.repo_root.resolve() / "repos.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog_through = date.fromisoformat(catalog["kenneyReleaseFeedThrough"])
        feed_through, entries = parse_feed(load_feed(args))
    except (OSError, KeyError, ValueError, json.JSONDecodeError, ET.ParseError) as error:
        print(f"audit failed: {error}", file=sys.stderr)
        return 2

    candidates = [
        entry for entry in entries if date.fromisoformat(entry.published) > catalog_through
    ]
    errors: list[str] = []
    if candidates and not args.skip_github:
        errors = matching_repositories(candidates, catalog.get("repos", []))

    for entry in candidates:
        if args.skip_github:
            entry.status = "candidate"
        elif entry.repositories:
            entry.status = "update"
        elif errors:
            entry.status = "unknown"
        else:
            entry.status = "new"

    if errors:
        status = "incomplete"
    elif candidates:
        status = "refresh-needed"
    elif date.fromisoformat(feed_through) < catalog_through:
        status = "incomplete"
        errors.append("official feed date is older than the catalog cutoff")
    else:
        status = "current"

    result = {
        "status": status,
        "feedThrough": feed_through,
        "catalogThrough": catalog_through.isoformat(),
        "candidates": [asdict(entry) for entry in candidates],
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        render_text(result)
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
