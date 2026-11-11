# Tileset provenance — maps/floor/tilesets/

`kc_base.png` and `kc_objects.png` are repacked selections (unmodified pixels,
rearranged into two compact sheets) from tilesets distributed with the
**official WorkAdventure preset world repositories**:

| Source sheet | Author / style | Taken from |
|---|---|---|
| `[Base]BaseChip_pipo.png` | Pipoya base chip | `github.com/workadventure/wam-preset-hackathon` |
| `1_Generic_32x32.png`, `6_Music_and_sport_32x32.png`, `13_Conference_Hall_32x32.png`, `14_Basement_32x32.png` | LimeZu room packs (WorkAdventure edition) | `github.com/workadventure/wam-preset-hackathon` |
| `tileset1.png`, `tileset_first_walls.png` | WorkAdventure | `github.com/workadventure/wam-preset-hackathon` |
| `modern_interiors_1.png`, `modern_interiors_2.png`, `walls_floor_tileset.png` | LimeZu Modern Interiors (WorkAdventure edition) | `github.com/workadventure/wam-preset-small-workshop` |

License: **“WORKADVENTURE SPECIFIC RESOURCES LICENSE”** as published in those
repositories’ `LICENSE.assets` (and mirrored in this repo’s `LICENSE.assets`):
the assets may be used and modified **only in maps produced for WorkAdventure**
(SaaS or self-hosted) and may be distributed **with such maps** — which is the
only way they are distributed here. They are **not** CC-licensed; do not reuse
these PNGs outside WorkAdventure maps.

Both map files (`study.tmj`, `arcade.tmj`) carry a `tilesetCopyright` property
pointing at this file. Packing scripts and the per-object extraction notes live
with the session scratchpad (`pack_tiles.py`, `extract*.py`); the object list
is `kc_pack.json` next to the sheets.
