/* KC Feature Lab — integrations bench (topics 14, 16 + webhooks).
 * Every third-party wire in one room: Discord Help Bell webhook, WidgetBot
 * read-only channel feed, event-results poster (reads the T17 tallies!),
 * open-data chest, CC BY-SA license checkpoint, community calendar embed.
 * ALL endpoints live in CONFIG below — empty string = graceful dry-run. */

var CONFIG = {
  helpHook:    "",  // Discord webhook URL → #help-desk
  resultsHook: "",  // Discord webhook URL → #event-log
  widgetbot:   "",  // e.g. https://e.widgetbot.io/channels/<server>/<channel>
  calendar:    "",  // public calendar embed URL
  wiki:        "https://github.com/DpenL/kanjiWorkAdv/wiki"
};
var siteHandle;
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Bench"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function onLeave(l, fn) { try { WA.room.onLeaveLayer(l).subscribe(fn); } catch (e) {} }
function post(hook, payload, okMsg) {
  if (!hook) { say("Dry run — webhook not configured (see CONFIG in scripts/lab/integrations.js). Payload would be: " + JSON.stringify(payload).slice(0, 140), "Webhook"); return; }
  fetch(hook, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
    .then(function () { say(okMsg, "Webhook"); })
    .catch(function () { say("Webhook POST failed — URL, CORS or rate limit. Note it.", "Webhook"); });
}
function sidebar(url) {
  try { return WA.ui.website.open({ url: url, position: { vertical: "top", horizontal: "right" }, size: { height: "100vh", width: "420px" } }); }
  catch (e) { try { WA.nav.openCoWebSite(url); } catch (e2) { say("Open manually: " + url); } }
}
function closeSite() { if (siteHandle && siteHandle.then) { siteHandle.then(function (w) { try { w.close(); } catch (e) {} }); } siteHandle = null; }
function getN(k) { try { return parseInt(WA.state[k], 10) || 0; } catch (e) { return 0; } }

WA.onInit().then(function () {
  onEnter("zone_topic16_help_button", function () {
    WA.ui.openPopup("help", "T16 · Help Bell: ping a human on Discord, they come TO you. Send?", [
      { label: "Send 🔔", className: "error", callback: function (p) {
          post(CONFIG.helpHook, { content: "🔔 **" + (WA.player.name || "Someone") + "** needs help — Feature Lab, integrations room" },
               "Helper pinged — stay put, they come to you.");
          p.close();
        } },
      { label: "Cancel", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic16_discord_feed", function () {
    if (!CONFIG.widgetbot) { say("T16 · WidgetBot feed: set CONFIG.widgetbot to https://e.widgetbot.io/channels/<server>/<channel> — read-only Discord inside the world. Dry run for now."); return; }
    siteHandle = sidebar(CONFIG.widgetbot);
  });
  onLeave("zone_topic16_discord_feed", closeSite);

  onEnter("zone_webhook_results", function () {
    var g = getN("kc_votes_green"), r = getN("kc_votes_red"), pillar = "";
    try { pillar = WA.state.kc_pillar || ""; } catch (e) {}
    WA.ui.openPopup("results", "Post current lab results to Discord? (🟢" + g + " / 🔴" + r + (pillar ? " · pillar: " + pillar.slice(0, 40) : "") + ")", [
      { label: "Post 📤", className: "primary", callback: function (p) {
          post(CONFIG.resultsHook, { embeds: [{ title: "Kanji Commons — lab session results",
              description: "🟢 works: **" + g + "** · 🔴 confusing: **" + r + "**" + (pillar ? "\npillar: " + pillar : "") + "\nvia in-world results-poster (topic 17→16 pipeline)" }] },
              "Results posted to #event-log — the async trail exists.");
          p.close();
        } },
      { label: "Cancel", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic14_asset_chest", function () {
    WA.ui.openPopup("chest", "T14 · Data-pack chest (all CC BY-SA / open, attribute EDRDG & KanjiVG):", [
      { label: "KANJIDIC2", className: "primary", callback: function (p) { try { WA.nav.openTab("http://www.edrdg.org/wiki/index.php/KANJIDIC_Project"); } catch (e) {} p.close(); } },
      { label: "KanjiVG", className: "primary", callback: function (p) { try { WA.nav.openTab("https://kanjivg.tagaini.net/"); } catch (e) {} p.close(); } },
      { label: "kanjiapi.dev", className: "primary", callback: function (p) { try { WA.nav.openTab("https://kanjiapi.dev/"); } catch (e) {} p.close(); } }
    ]);
  });

  onEnter("zone_topic14_submission_desk", function () {
    WA.ui.openPopup("license", "T14 · Submission checklist — before your demo goes to the gallery:\n☐ EDRDG/KanjiVG attribution shown in-app\n☐ CC BY-SA share-alike honored\n☐ repo licence file present", [
      { label: "All confirmed ✓", className: "success", callback: function (p) {
          say("Accepted — a checklist, not a locked door (per the no-gates rule).", "Registrar");
          post(CONFIG.resultsHook, { content: "📥 " + (WA.player.name || "someone") + " confirmed license compliance for a gallery submission" }, "Logged to Discord.");
          p.close();
        } },
      { label: "Read licence", className: "normal", callback: function (p) { try { WA.nav.openTab("http://www.edrdg.org/edrdg/licence.html"); } catch (e) {} p.close(); } }
    ]);
  });

  onEnter("zone_calendar", function () {
    if (!CONFIG.calendar) { say("Calendar embed: set CONFIG.calendar (public Google Calendar / Nextcloud embed URL). Decentralized events — anyone can host a book corner or seminar. Dry run."); return; }
    siteHandle = sidebar(CONFIG.calendar);
  });
  onLeave("zone_calendar", closeSite);
}).catch(function (e) { console.error("[lab integrations]", e); });
