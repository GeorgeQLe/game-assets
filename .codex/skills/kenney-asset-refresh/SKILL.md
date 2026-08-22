---
name: kenney-asset-refresh
description: Audit Kenney's official release feed against GeorgeQLe/game-assets and its indexed assets-* repositories, then import and catalog missing or updated packs when the user requests a periodic Kenney asset refresh. Use for Kenney refresh checks, catalog synchronization, or importing newly released Kenney packs; do not use for unrelated project assets or the IT asset-inventory-db application.
---

# Kenney Asset Refresh

Keep the central catalog and its indexed asset repositories synchronized with
Kenney's official release feed. A refresh can be a read-only audit or an applied
multi-repository update, depending on the user's request.

## Start with the audit

Run from the `game-assets` repository root:

```bash
python3 .codex/skills/kenney-asset-refresh/scripts/audit_kenney_feed.py
```

The helper compares the official RSS feed with
`repos.json.kenneyReleaseFeedThrough`. For feed entries after that cutoff, it
uses `gh api` to identify matching source URLs in the indexed repositories.

- `CURRENT` means no feed entry is newer than the catalog cutoff. Report the
  feed date and make no changes.
- `NEW` means the feed entry is not found in any indexed manifest.
- `UPDATE` means the slug already exists and Kenney published a newer feed
  entry. Re-download and compare it; presence alone does not prove that the
  stored copy is current.
- `UNKNOWN` means one or more manifest lookups failed, so an unmatched entry
  cannot safely be classified as new.
- Treat feed or GitHub lookup failures as an incomplete audit. Do not advance
  the cutoff.

The official feed and asset pages are the authority:

- `https://kenney.nl/feed`
- `https://kenney.nl/assets/<slug>`

Do not infer freshness from search-engine ordering, repository `updated_at`, or
the separate `GeorgeQLe/assets` image repository.

## Apply a refresh only when requested

An audit/check request is read-only. A request to refresh, sync, download, or
store new assets authorizes changes to `game-assets` and the indexed destination
repositories required for the identified Kenney entries. It does not authorize
changes to unrelated repositories.

When the audit finds candidates, read
[references/catalog-contract.md](references/catalog-contract.md) before making
changes. Follow its routing, download, manifest, validation, and commit rules.

Use a temporary directory for downloads and clone only the destination
repositories needed for the refresh. Preserve dirty user work in any existing
checkout; use a separate clean checkout if necessary.

## Completion conditions

Finish only when one of these is true:

1. The official feed is not newer than the catalog and the result is reported as
   a no-op.
2. Every candidate pack is downloaded from its official page, stored in an
   appropriate indexed repository, licensed, cataloged, validated, committed,
   and pushed; then the central cutoff and refresh summary are committed and
   pushed last.
3. A destination or source cannot be determined safely. Report the exact pack
   and unresolved choice without advancing the central cutoff.

Report the feed date, candidates, destination repositories, validation results,
and pushed commit IDs. Never create a no-op commit merely to record that a check
ran.
