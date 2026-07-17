# Onboarding & accessibility playbook

**Why this file exists:** the research is unambiguous — felt competence with the tool, not co-presence, decides whether non-gamers (our educators) come back. So onboarding is a first-class module, not polish.

## The funnel
1. **Landing page** (`web/index.html`) — 60-second orientation *before* the world: what it looks like, mic permission warning, movement keys. Never send a bare map link.
2. **Genkan** (`maps/genkan.tmj` + `scripts/genkan.js`) — small enclosed room: pick language (EN/JA tiles), try one voice bubble, then walk through the torii. Can't get lost; nothing is forced.
3. **Help Bell** — 🔔 button in the toolbar on every map; pings a Discord channel via webhook so a human greeter comes *to the person*.
4. **Greeter rota** (ops) — during events, one named person per hour whose only job is welcoming; the research on failed spaces keeps pointing at the absence of this.
5. **Practice session** (ops) — 30 minutes, days before an event, for anyone who wants to try controls without an audience.

## Hard rules adopted
- **No forced tutorials, no locked doors, no timers.** Opt-in quests (stamp rally) only.
- **Text-mirror principle:** every kiosk is also a plain web page; nothing essential exists only inside the world.
- **Bilingual by default:** every guide string ships EN + JA (see `scripts/genkan.js` STR table).
- **Keyboard-only must work; reduced-motion respected** in kiosk pages (`style.css`).

## Known limits (honest)
Avatar platforms have documented accessibility problems (screen-reader support, voice-driven navigation). The text-mirror principle is our mitigation, not a solution — offer a parallel non-spatial path (Discord + wiki + video call) for anyone who needs it, without making it feel second-class.
