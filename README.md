# Game Assets Index

Central catalog for all game asset repositories. Each repo follows a consistent structure with machine-readable manifests, license tracking, and tagged metadata.

## Latest Kenney Refresh

Synced through Kenney's release feed dated **2026-08-18**. This refresh added Pattern Pack Extra, Domino Pack, Mini Dungeon, Skyboxes, Mini Forest, Modular Cave Kit, Tiny Farm, and Flag Pack, and updated City Kit (Roads), Crosshair Pack, and Input Prompts.

## Repositories

### 2D Assets
| Repo | Description |
|------|-------------|
| [assets-2d-space](https://github.com/GeorgeQLe/assets-2d-space) | Ships, planets, stations, asteroids, backgrounds |
| [assets-2d-castle](https://github.com/GeorgeQLe/assets-2d-castle) | Walls, towers, characters, props |
| [assets-2d-city](https://github.com/GeorgeQLe/assets-2d-city) | Buildings, roads, vehicles, props |
| [assets-2d-nature](https://github.com/GeorgeQLe/assets-2d-nature) | Trees, terrain, water, animals, foliage |
| [assets-2d-isometric](https://github.com/GeorgeQLe/assets-2d-isometric) | Isometric tiles, buildings, props, characters |
| [assets-2d-characters](https://github.com/GeorgeQLe/assets-2d-characters) | Toon, pixel, animated character sprites |
| [assets-2d-items](https://github.com/GeorgeQLe/assets-2d-items) | Weapons, potions, loot, collectibles |
| [assets-2d-prototyping](https://github.com/GeorgeQLe/assets-2d-prototyping) | Placeholder and development assets |

### 3D Assets
| Repo | Description |
|------|-------------|
| [assets-3d-city](https://github.com/GeorgeQLe/assets-3d-city) | Roads, buildings, vehicles, suburban |
| [assets-3d-nature](https://github.com/GeorgeQLe/assets-3d-nature) | Terrain, trees, rocks, water, foliage |
| [assets-3d-space](https://github.com/GeorgeQLe/assets-3d-space) | Ships, stations, asteroids, planets |
| [assets-3d-medieval](https://github.com/GeorgeQLe/assets-3d-medieval) | Castles, towers, siege, village |

### KayKit 3D Assets
| Repo | Description |
|------|-------------|
| [assets-kaykit-3d-characters](https://github.com/GeorgeQLe/assets-kaykit-3d-characters) | Characters, rigs, animation sets, skeletons, mystery monthly characters |
| [assets-kaykit-3d-environments](https://github.com/GeorgeQLe/assets-kaykit-3d-environments) | World, environment, terrain, dungeon, city, platformer, medieval, space base kits |
| [assets-kaykit-3d-props](https://github.com/GeorgeQLe/assets-kaykit-3d-props) | Props, items, tools, weapons, furniture, resources, tabletop pieces, prototype bits |

### UI Assets
| Repo | Description |
|------|-------------|
| [assets-ui-elements](https://github.com/GeorgeQLe/assets-ui-elements) | Panels, buttons, cursors, badges, frames |
| [assets-ui-icons](https://github.com/GeorgeQLe/assets-ui-icons) | Inventory, skills, status, navigation icons |

### Sound Effects
| Repo | Description |
|------|-------------|
| [assets-sfx-ui](https://github.com/GeorgeQLe/assets-sfx-ui) | Clicks, hovers, notifications, menus |
| [assets-sfx-combat](https://github.com/GeorgeQLe/assets-sfx-combat) | Impacts, explosions, weapons, hits |
| [assets-sfx-ambient](https://github.com/GeorgeQLe/assets-sfx-ambient) | Environment, weather, atmosphere |
| [assets-sfx-voice](https://github.com/GeorgeQLe/assets-sfx-voice) | Voiceovers, callouts, grunts, dialogue |

### Music, VFX & Fonts
| Repo | Description |
|------|-------------|
| [assets-music](https://github.com/GeorgeQLe/assets-music) | Music tracks: ambient, battle, menu, exploration |
| [assets-vfx-particles](https://github.com/GeorgeQLe/assets-vfx-particles) | Explosions, trails, impacts, magic effects |
| [assets-fonts](https://github.com/GeorgeQLe/assets-fonts) | Game-ready fonts with license metadata |

## Repo Structure (each repo)

```
assets-<name>/
├── assets/          # Original or normalized asset files
├── previews/        # Thumbnails and contact sheets
├── LICENSES/        # Original license files
├── examples/        # Tiny usage previews
├── manifest.json    # Machine-readable asset index
├── tags.json        # Genre, theme, style tags
└── README.md
```

## Manifest Entry Format

```json
{
  "id": "kenney-city-kit/building-townhall-01",
  "name": "Townhall 01",
  "path": "assets/kenney/city-kit/buildings/townhall_01.png",
  "preview": "previews/townhall_01.png",
  "source": "Kenney City Kit",
  "sourceUrl": "https://kenney.nl/assets/...",
  "license": "CC0-1.0",
  "tags": ["2d", "city", "building", "isometric"],
  "fileType": "png",
  "dimensions": { "width": 256, "height": 256 }
}
```

## Adding Assets

1. Clone the appropriate repo
2. Place assets in `assets/<source-pack>/`
3. Add license to `LICENSES/`
4. Generate preview in `previews/`
5. Add entry to `manifest.json` with all required fields
6. Tag in `tags.json` or in the manifest entry

## Refreshing Kenney Assets

This repository tracks the repo-specific `$kenney-asset-refresh` Codex skill.
Ask Codex to use it for a periodic check or to apply a refresh. The skill audits
Kenney's official release feed, cross-references indexed manifests, imports new
or updated packs into the appropriate asset repositories, and advances this
catalog only after destination changes are validated and pushed.
