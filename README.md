# Game Assets Index

Central catalog for all game asset repositories. Each repo follows a consistent structure with machine-readable manifests, license tracking, and tagged metadata.

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
| [assets-3d-worlds](https://github.com/GeorgeQLe/assets-3d-worlds) | 3D buildings, terrain, props, vehicles, kits |

### UI Assets
| Repo | Description |
|------|-------------|
| [assets-ui-elements](https://github.com/GeorgeQLe/assets-ui-elements) | Panels, buttons, cursors, badges, frames |
| [assets-ui-icons](https://github.com/GeorgeQLe/assets-ui-icons) | Inventory, skills, status, navigation icons |

### Audio
| Repo | Description |
|------|-------------|
| [assets-sfx](https://github.com/GeorgeQLe/assets-sfx) | Sound effects: impacts, UI, ambient, character, environment |
| [assets-music](https://github.com/GeorgeQLe/assets-music) | Music tracks: ambient, battle, menu, exploration |

### VFX & Fonts
| Repo | Description |
|------|-------------|
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
