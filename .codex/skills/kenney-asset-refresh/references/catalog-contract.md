# Game Asset Catalog Contract

Read this reference only when a Kenney audit finds a new or updated feed entry
that the user asked to apply.

## Repository boundary

`game-assets/repos.json` is the destination allowlist and central index. Modify
only `GeorgeQLe/game-assets` and the listed destination repositories needed for
the refresh. `GeorgeQLe/assets` and `asset-inventory-db` are outside this
workflow.

For an update, keep the pack in the repository that already contains its
`sourceUrl`. For a new pack, choose the narrowest existing repository whose
category and theme match the pack page:

| Pack characteristics | Destination |
| --- | --- |
| 2D space | `assets-2d-space` |
| 2D castle or medieval scenery | `assets-2d-castle` |
| 2D city, roads, or urban scenery | `assets-2d-city` |
| 2D nature, terrain, farming, plants, or animals | `assets-2d-nature` |
| 2D explicitly isometric | `assets-2d-isometric` |
| 2D character sheets or animations | `assets-2d-characters` |
| 2D items, loot, cards, board-game pieces, or collectibles | `assets-2d-items` |
| 2D placeholders or prototyping aids | `assets-2d-prototyping` |
| 3D city, roads, vehicles, or urban scenery | `assets-3d-city` |
| 3D nature, terrain, general environments, skyboxes, or caves | `assets-3d-nature` |
| 3D space | `assets-3d-space` |
| 3D medieval, castle, or dungeon | `assets-3d-medieval` |
| UI panels, controls, cursors, or frames | `assets-ui-elements` |
| UI, input, flag, crosshair, inventory, or status icons | `assets-ui-icons` |
| Particle-ready textures, patterns, masks, explosions, or VFX | `assets-vfx-particles` |
| UI, combat, ambient, or voice audio | The matching `assets-sfx-*` repo |
| Music | `assets-music` |
| Fonts | `assets-fonts` |

The `assets-kaykit-*` repositories are KayKit-specific; do not place Kenney
packs in them. If a new pack fits multiple destinations equally or none safely,
stop and request a destination choice instead of creating a repository or using
a generic dumping ground.

## Official download and archive handling

1. Fetch `https://kenney.nl/assets/<slug>` and extract the ZIP URL from the
   `Continue without donating` link (`id='donate-text'`). Download only from
   `kenney.nl/media/pages/assets/...`.
2. Download into a newly created temporary directory. Record the ZIP SHA-256 in
   the work log or final report.
3. Verify the response is a ZIP and run `unzip -t` before extraction. Inspect the
   archive member list for absolute paths or `..` traversal before extracting.
4. Extract into `assets/kenney/<slug>/`. Preserve Kenney's formats, directory
   structure, samples, and source files. For an update, compare against the
   tracked directory and remove obsolete pack files only when the new official
   archive clearly supersedes them.
5. Copy Kenney's supplied license text to
   `LICENSES/kenney-<slug>-license.txt`. Keep the original license wording.

Do not use third-party mirrors or the paid All-in-1 bundle as the source for an
individual refresh.

## Destination repository updates

Follow the destination repository's existing `manifest.json`, `tags.json`, and
README conventions. At minimum:

- Add manifest entries for the same usable file extensions already cataloged by
  that repository. Exclude license and descriptive metadata files unless the
  existing manifest includes them.
- Use a stable ID prefixed with `kenney-<slug>/`, the tracked relative path,
  human-readable name, `https://kenney.nl/assets/<slug>` as `sourceUrl`,
  `CC0-1.0`, and useful category/theme/pack tags.
- Set `totalAssets` to the actual length of the `assets` array and add the pack
  to `sources` once.
- Update the README pack list and asset totals. Update `tags.json` only when its
  current schema requires a new tag.
- For a pack update, replace that pack's manifest entries rather than appending
  another copy.

Some existing manifests contain duplicate IDs inherited from older imports.
Do not broaden a periodic refresh into a full migration. Ensure the changed
pack's new IDs are unique and that the repository-wide duplicate-ID count does
not increase. Paths must remain unique.

## Validation

Before committing a destination repository, verify:

- the official ZIP passes integrity checks;
- every manifest path exists and is tracked;
- the changed pack has no duplicate IDs or paths;
- repository-wide duplicate IDs did not increase;
- `totalAssets == assets.length` and `sources` contains the pack exactly once;
- the dedicated CC0 license exists;
- JSON files parse, `git diff --check` passes, and only intended pack/catalog
  files changed.

Commit and push each destination repository before changing the central index.
Use a concise commit such as `Refresh Kenney <Pack Name> assets`.

## Central index transaction

After every destination commit is successfully pushed:

1. Set `repos.json.kenneyReleaseFeedThrough` to the feed's `lastBuildDate` date.
2. Bump the central catalog minor version for pack additions or source updates;
   use a patch bump only for metadata-only corrections.
3. Replace README's `Latest Kenney Refresh` paragraph with the new cutoff and a
   concise added/updated pack summary.
4. Validate `repos.json`, run `git diff --check`, commit, and push
   `game-assets` last.

Never advance the cutoff past an unprocessed candidate. If one destination push
fails, leave the central index unchanged and report which destination commits
were already pushed so the next run can resume safely.
