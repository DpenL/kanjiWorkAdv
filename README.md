# 漢字コモンズ · Kanji Commons

A modular WorkAdventure world for the kanji-learning-games community — educators, game
engineers, designers and researchers. Built as separate rooms you can grow, reskin and let
others extend.

```
kanji-commons/
├── maps/            Tiled maps (.tmj) + placeholder tileset
│   ├── genkan.tmj     entry & tutorial room (language pick, voice-bubble demo)
│   ├── commons.tmj    stage · breakout · library kiosks · board · karaoke corner
│   └── tileset.png    generated placeholder — swap for a real Japanese tileset
├── scripts/         plain-JS WorkAdventure map scripts (no build step)
│   ├── genkan.js      bilingual guide, language tiles, 🔔 Help Bell (Discord webhook)
│   └── commons.js     zone hints, stamp rally, 📅📖💬🔔 toolbar ("smartphone lite")
├── web/             kiosk pages opened by zones (all also work as normal pages)
│   ├── index.html     web-first landing / orientation  ← send people HERE, not the map
│   ├── library.html   curated data/API/paper resources + license panel
│   ├── kanji-quiz.html  live mechanic demo vs kanjiapi.dev (KANJIDIC2)
│   ├── tracing.html   KanjiVG stroke-order animation kiosk
│   ├── board.html     common-room board (persistence placeholder) + ema wall
│   └── karaoke.html   karaoke corner how-to
├── docs/            DESIGN.md (idea catalog) · DECISIONS.md · ONBOARDING.md
├── gen_maps.py      regenerates maps + tileset (edit layouts here, not in raw JSON)
└── .github/workflows/deploy.yml   GitHub Pages deploy
```

## Quick start (no self-hosting needed)
1. Push this folder to a **public** GitHub repo and enable **Pages** (Settings → Pages →
   Source: GitHub Actions). The included workflow publishes everything.
2. Open your world at:
   `https://play.workadventu.re/_/global/<user>.github.io/<repo>/maps/genkan.tmj`
3. Put that URL behind the button in `web/index.html` (`PLAY_URL`) and share the
   **index.html** link — never the raw map link (onboarding funnel, see docs/ONBOARDING.md).

## Editing
- **Layouts:** edit `gen_maps.py` and rerun (`python3 gen_maps.py`), or open the `.tmj`
  files directly in [Tiled](https://www.mapeditor.org/). Zones are tile layers whose
  properties (`jitsiRoom`, `openWebsite`, `silent`, `exitUrl`) drive all behavior.
- **Scripts:** plain JS, defensive against API differences; wire your links in the
  `LINKS`/`DISCORD_HELP_WEBHOOK` constants at the top.
- **New rooms:** one new `.tmj` + an `exitUrl` zone from an existing map. That's the whole
  contribution model — community members can PR a room without touching anything else.
- **Art:** the tileset is a generated placeholder. Swap in a real Japanese-themed 2D
  tileset (itch.io / OpenGameArt; check the license allows redistribution in a public repo).

## Testing checklist before your first event
- [ ] Walk genkan → commons and back; try every SPACE kiosk
- [ ] Confirm each kiosk page loads inside the iframe (some future embeds will be blocked
      by X-Frame-Options — test early, fall back to new-tab links)
- [ ] Wire and test the Help Bell webhook; staff a greeter
- [ ] Dry-run with 3–4 friends on the free hosted tier (≈15 concurrent cap)

## Licensing
Code: MIT. Dictionary/stroke data shown by kiosks: © EDRDG / KanjiVG under CC BY-SA —
the visible credits in the kiosk footers are a license requirement, keep them.
