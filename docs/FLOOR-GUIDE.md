# Demo Floor (online) — guide

The session-1 demo floor as a shareable WorkAdventure room — and the seed of a
**museum/arcade world we keep extending**: every exhibit is a reusable
**Demostand**, the floor plan around them is provisional on purpose.

```
https://play.workadventu.re/_/global/dpenl.github.io/kanjiWorkAdv/maps/floor/floor.tmj
```

Anonymous/public route — fine for a shared tour link. Research-corpus figure:
WA free tier ≈ **10 concurrent** users (shrank from 14; re-verify before inviting more at once).

## The Demostand (the unit everything is built from)
One demo = one stand = **terminal + poster + walk-up pad + voice table**:

- **Pad** (lantern tiles): walk on → the poster popup (blurb + try-prompt;
  **▶ Open** launches the demo and that's what earns the stamp).
- **Voice table** (dark ring around the pad, jitsi `onaction`): anyone in the
  ring gets a *"〈name〉 voice table — watch & discuss / Enter Jitsi"* banner.
  One person plays and **screen-shares in the jitsi**; the others stand next
  to them, watch and talk. No auto-join — it never grabs your mic uninvited.
- **Terminal + poster tiles** are solid (per-map `collides` on this map's
  tileset entry only — the shared placeholder PNG and the other maps are untouched).

### Add / swap a demo (the whole recipe)
1. `gen_floor_maps.py` → add a line to `STANDS` (slug, label, side L/R, y).
2. `scripts/floor/floor.js` → add the matching entry to `CONFIG.stands`
   (same slug; blurb/prompt/url; `embed: true` only if the host allows iframes).
3. `py gen_floor_maps.py` · `node --check scripts/floor/floor.js` · run the
   validator (scratchpad `check_floor.py`: slugs, anchors, walkability with
   solid furniture, zone disjointness, voice-ring-covers-pad) · push.

## The six stands today
| Stand | Kind | Online today | ✎ yours to fill (CONFIG in `scripts/floor/floor.js`) |
|---|---|---|---|
| DragonTale | 🕹 arcade | poster only | `url` when a web build exists |
| Radical Fighters | 🕹 arcade | poster only | `poster` (your one-liner) + `url` |
| Music to My Ears / Maji Kana | 🕹 arcade | poster only | `poster`, `prompt`, `url` (build availability was already ✎ on the physical floor) |
| WaniKani | 🏛 museum | ▶ opens wanikani.com (new tab) | — |
| Anki (plain deck) | 🏛 museum | ▶ opens ankiweb.net (new tab) | — |
| Duolingo (Japanese) | 🏛 museum | ▶ opens duolingo.com (new tab) | — |

Blurbs verbatim from the session-1 game profiles (`deck_data.py` PROFILES);
✎-gapped ones ship empty rather than invented. Museum links open in a new tab
on purpose (X-Frame-Options). A future own-game web build can set `embed: true`
to open as an in-world co-website — and could even talk back over the
scripting API (`allowApi`) to stamp on *completion* instead of launch.

## Completion quest (stamp rally) — honest edition
- **A stamp = you actually opened the demo** (the ▶ Open button). Clicking
  through a poster alone no longer counts.
- **Stands without an online build don't count toward the total** — the rally
  is "try everything that's online", currently 3/3 (the museum wall), and the
  total grows as game builds get wired in.
- Progress: the **🎮 n/m button in the top bar** (click → bulleted list in
  chat) and the 🏆 trophy popup (shows the missing stands by name). Welcome
  message points at both; per-player persistence via `WA.player.state`.
- All wired stands → chat fanfare, finisher counter at the trophy
  (world variable `kc_floor_finishers`, best-effort on the public route — a toy,
  not a metric), nudge to leave a line on the 📌 board. Opt-in; nothing locked.

## Other zones
- **📜 Poster wall** — `CONFIG.posterUrl`, ships **empty** (graceful popup).
- **📌 Board** — `CONFIG.boardUrl` → the existing `web/board.html` kiosk.
- **🍵 Floor café** — always-on jitsi corner (auto-join on the tatami),
  chat hint debounced to once a minute.
- **→ 玄関** exit back to the genkan map.

## Re-skin drafts (10 Nov) — pick a direction
The placeholder look is a 16-slot palette tileset; a **skin = another 16-slot
tileset image** (same slot semantics: floor, wall, poster, screen, body, pad,
ring tint …), so swapping the map's tileset re-skins the whole floor without
touching layout or script. Two drafts were composed from real assets and
rendered over the actual floor.tmj (`docs/img/skin-draft-*.png`):

- **A · Cozy study/museum** (quiet, homely): LimeZu-style interiors from the
  official WA preset worlds — calm beige floor, olive shell, framed posters,
  display booths, plant nook. Fits "library/study" with bookshelf/desk stands.
- **B · Arcade** (dark + neon): Kenney 1-bit (CC0) — dark checker floor, brick
  shell, cabinets with 👾 invader screens, crowns on the trophy plinth.
  (Real build needs light label text — ink text vanishes on dark floors.)

Options beyond one skin: **two rooms** (literature/study wing vs games wing,
each its own skin, linked by exits) — the stand unit and script are already
room-agnostic; or keep both skins as alternate tileset files and switch per
event. Stand visuals per skin can differ (terminal / bookshelf / shrine /
microscope…) by swapping the three deco slots.

### Asset inventory (local, license-checked)
| Source | Where | License | Fit |
|---|---|---|---|
| Kenney 1-bit pack 1.1 | `Downloads/kanjiGameAssets/1bitpack_kenney_1.1.zip` | **CC0** | arcade skin (colored_packed, 16px→2×) |
| Kenney Roguelike pack | same folder | **CC0** | props/variety, 16px |
| Zelda-like (ArMM1998) `gfx.zip` | same folder | **CC0** | cozy homely alternative, 16px |
| LimeZu-style WA edition (modern/office interiors, walls_floor, posters) | `reference-worlds/wam-preset-*/tilesets/` | **"WorkAdventure specific resources license"**: use + distribution allowed *with maps produced for WorkAdventure* (LICENSE.assets in those repos); not CC — keep usage inside WA maps and carry the license text in a COPYRIGHT file | cozy skin, 32px native, the polished look |
| LPC sets (Tuto clone) | `workadventure/maps/Tuto/tilesets/` | CC-BY-SA 3.0 / GPL 3.0 (attribution files beside them) | 32px, outdoor + specials |
| Curated link library (per-theme, license-classed) | `Documents/virtual-event-space-research/APPENDIX-ASSET-LIBRARY.md` | — | when a skin needs more (e.g. GuttyKreum JP sets are 🟡 no-redistribution → gray zone on public Pages) |

**Public-map rule** (from the research corpus): WA serves tileset PNGs as
downloadable files, so on the public Pages route stick to CC0/CC-BY or the
WA-maps-only license above; record author·license·version·URL per asset in a
`COPYRIGHT` file and mirror into `tilesetCopyright`.

## Known state
- **Live since 10 Nov 2026**, floor v2 (`bfba815`, `92a5c41`): demostands,
  honest quest gating, voice tables, solid furniture, compact popups,
  layout-agnostic greeter, café debounce.
- Live-verified (anonymous walkthrough, fresh session): welcome + bulleted
  rally list render line-by-line in chat; 🎮 top-bar counter shows wired-only
  total (1/3 with the tester's old stamps); unwired stand popup = poster +
  "⏳ coming soon", OK only, no stamp; voice-table banner "Maji Kana voice
  table — watch & discuss / Enter Jitsi" appears in the ring; furniture
  collision holds (can't walk onto cabinets).
- Not yet exercised live: ▶ Open stamping after the gating change (same code
  path as before, now the only stamp path), full 3/3 fanfare + finisher
  counter (left for a real first finisher), genkan exit, two-player
  screen-share in a stand jitsi.
- Earlier (floor v1) live-verified: all popup variants, stamps + badge,
  persistence across reloads, café jitsi auto-join; two v1 bugs fixed
  (café/Duolingo zone overlap; stale popup refs).
- WA popups collapse newlines → popups stay single-flow; lists go to chat
  (chat renders `•`-bulleted lines as a proper list).
- Static checks (rerun after any regen): JSON/layer sizes, JS syntax,
  zone↔CONFIG slugs, popup anchors, start-to-every-zone walkability with
  solid furniture, zone disjointness, voice-ring ⊇ pad.
