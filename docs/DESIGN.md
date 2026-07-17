# Kanji Commons — merged design catalog

Origin tags: **[C]** Claude research report · **[G]** Gemini session · **[N]** new in this pass.
Everything is a *separate module* (a room `.tmj`, a script, or a web kiosk). Nothing here removes anything from [C] or [G] — additions only, per David's instruction.

## 1. World structure
- **[C]** Campus building MVP (stage / breakout / commons / library) → built: `maps/commons.tmj`
- **[G]** Virtual Ryokan & Arcade skin; Genkan entry room → built: `maps/genkan.tmj`
- **[C]** Village/districts with community plots (deferred until content exists)
- **[G]** Modular multi-map linking via exit layers (adopted: genkan ⇄ commons)
- **[N] Seasonal skinning** — sakura / matsuri / momiji tileset variants per season or event; cheap re-fresh that makes returning feel new
- **[N] Torii research path** — a Fushimi-Inari-style gate path where each gate is a stage of the research pipeline (idea → prototype → playtest → publish), each with its own station; doubles as methodology teaching for engineers new to research

## 2. Onboarding & accessibility
- **[G]** Web-first buffer landing page → built: `web/index.html`
- **[G]** Genkan 1-room tutorial (language pick, voice-bubble demo) → built: `scripts/genkan.js`
- **[G]** Help Bell → Discord webhook → built (placeholder URL) in both scripts
- **[C]** Human greeter role + pre-event practice session (ops, not code)
- **[G]** Ghost-guide floor path (footprint tiles) — planned, pure tileset work
- **[N] Text-mirror principle** — every kiosk is a normal web page too, so screen-reader users and iframe-blocked clients lose nothing; adopted as a hard rule for all future kiosks
- **[N] Barrier-free map twin** — high-contrast, large-tile variant of each room generated from the same generator script (the generator makes this nearly free)

## 3. Event mechanics
- **[C]** Poster gallery, demo booths, BoF tables, translation-relay, grounding arcade
- **[G]** 20-topic matrix (stage/megaphone, speed-dating rings, pitch arena, checkpoint teleporters, polling carpets, trophy room, expo hall …) — kept as the option menu for event design
- **[N] Stamp rally (スタンプラリー)** — opt-in exploration quest across rooms; culturally native, zero coercion → built: `scripts/commons.js`
- **[N] Kamishibai lightning talks** — paper-theater frame on the stage for low-pressure 5-minute talks; gentler entry to presenting than the keynote megaphone
- **[N] Radio-taisō break bell** — scheduled group stretch for multi-day online events; a shared ritual that fights screen fatigue and builds community identity
- **[N] Zabuton queue** — cushion tiles forming a visible, orderly queue for office hours / mentor sessions

## 4. Persistence & async (DE–JP time zones)
- **[C]** Artifact persistence: “leave results on the board” → `web/board.html` + house rule
- **[G]** Wiki = source of truth, Discord = async pulse, WA = synchronous venue (adopted as architecture)
- **[G]** Virtual smartphone overlay → built lite as action-bar buttons (📅 📖 💬 🔔) in `scripts/commons.js`
- **[N] Ema wall (絵馬)** — goals written at event start, revisited at closing → seeded in `web/board.html`
- **[N] Pixel garden** — a zen-garden corner that visibly grows one element per artifact left behind (post, demo, paper); an ambient aliveness meter that counters the dead-space feeling
- **[N] Konbini** — a tiny convenience-store room for grab-and-go: prepared JSON data packs, sprite assets, template repos; the [G] “item chest” idea given a Japanese skin and a fixed place

## 5. Domain kiosks (kanji · pedagogy · engineering)
- **[C]** Library / resource hub → built: `web/library.html` (incl. license panel)
- **[C]+[G]** Live dictionary kiosk → built: `web/kanji-quiz.html` (kanjiapi.dev)
- **[G]** KanjiVG tracing canvas → built as animation kiosk: `web/tracing.html` (tracing input = next step)
- **[G]** FSRS sandbox, Leitner-box room, radical-decomposition lab, cognitive-load testbench — queued kiosks, all fit the same web/ + zone pattern
- **[C]** Genre museum (mostly video/link panels + few live embeds) — queued room
- **[N] Glyph-creature greeters** — David's sprite-generator kanji creatures as decorative NPCs/mascots per room; ties an existing project in and gives the space a unique identity no template has
- **[N] Confusables gallery** — wall exhibit of easily-confused kanji pairs (己/已/巳 …) as a conversation piece that teaches while you idle

## 6. Community & identity
- **[C]+[G]** Discipline-visible avatars / role nameplates ([DEV]/[EDU]/[RES])
- **[C]** Community plots with light governance (upload rights, theme guide, cleanup)
- **[N] Nomikai room** — izakaya table next to karaoke for post-event decompression; socials need a *place*, not just leftover time
- **[N] Interlingual name ceremony** — new members pick/receive a kanji nickname at a small shrine kiosk; cheap ritual, strong belonging signal, on-domain
