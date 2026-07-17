# Open decisions & review notes

## Review notes on the Gemini session (additive — nothing removed)
1. **Virtual smartphone**: concept adopted (built lite via `WA.ui.actionBar`). Caveat: the full modal-overlay version depends on newer scripting-API surface that differs between SaaS and self-hosted versions — verify on the target version before building deep. The lite version degrades gracefully.
2. **Discord OAuth pass-through** (“align identities by passing OAuth tokens through WA variables”): overstated as described — practical on self-hosted WA with a custom auth flow, not on the free SaaS. Treat as a self-hosting-phase feature; webhooks (Help Bell) are the honest MVP integration.
3. **“Programmatically enforce research positioning”**: recommend softening. Locked gates and mandatory checkpoints contradict the no-forced-game-logic principle David set; curation, affordances and defaults steer better than gates. The license checkpoint survives as a *submission-form checklist*, not a door.
4. **Megaphone / jitsiRoomAdminTag**: depends on admin/tag features that differ by plan and hosting mode — test early on the hosted tier before promising a keynote format.
5. Genkan, web-first buffer, modular exit-layer architecture, wiki/Discord/WA triad: all sound, all adopted.

## Decisions David still owns
1. **Debut strategy** — first workshop live in the space, or space debuts as the workshop's archive?
2. **Theme depth vs speed** — placeholder tiles now + real Japanese tileset later (current path), or invest in art before the first event?
3. **Library curation** — solo-curated, wiki-open, or curated core + submission queue?
4. **Async backbone** — create the Discord now (recommended: Help Bell needs it anyway)?
5. **Success metric** — returning visitors, artifacts left per event, or cross-discipline connections? Decides which modules get built next.
6. **Self-host trigger** — >15 concurrent expected, custom auth wanted, or GDPR/participant-data needs: whichever comes first.
