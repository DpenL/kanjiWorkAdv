/* Demo Floor — online. Six stations (3 arcade cabinets = the kanji games,
 * 3 museum plaques = the industry specimens), a stamp rally across all six,
 * a trophy pedestal with a finisher counter, poster wall + common board.
 * Same conventions as scripts/commons.js / scripts/lab/*: plain JS, CONFIG
 * block on top, everything degrades gracefully when a URL is empty. */

// ---- config (edit me) -------------------------------------------------------
var CONFIG = {
  stations: [
    // kind "arcade" = playable kanji games (cabinets). url empty = cabinet not
    // wired to an online build yet; the popup still shows and still stamps.
    { slug: "dragontale", kind: "arcade", name: "DragonTale",
      blurb: "RPG for learning Japanese kanji, developed and iterated at TUM over several years.",
      prompt: "Play the opening minutes without help. Note the first moment the game teaches you a kanji — how does it do it?",
      url: "", embed: false },                                   // ✎ web build URL when one exists
    { slug: "radfighters", kind: "arcade", name: "Radical Fighters",
      blurb: "",                                                  // ✎ David's one-liner (PoC on the KanKyouKen platform)
      prompt: "Play one round. Watch what the game seems to notice about you while you play.",
      url: "", embed: false },                                   // ✎ build URL
    { slug: "majikana", kind: "arcade", name: "Music to My Ears / Maji Kana",
      blurb: "",                                                  // ✎ confirm build availability (as on the physical floor)
      prompt: "",
      url: "", embed: false },                                   // ✎ build URL
    // kind "museum" = look-and-compare exhibits; links open in a new tab
    // (these sites refuse to be iframed — embed stays false on purpose).
    { slug: "wanikani", kind: "museum", name: "WaniKani",
      blurb: "Commercial web app: spaced repetition for ~2,000 kanji and ~6,000 words, taught through mnemonics and levels. Not a game in the play sense — a provocation about what “gamified” means.",
      prompt: "Do a few review items. Notice what it does when you get one wrong — and how that feels.",
      url: "https://www.wanikani.com", embed: false },
    { slug: "anki", kind: "museum", name: "Anki (plain deck)",
      blurb: "The baseline: a free SRS flashcard app with a community kanji deck. Pure repetition, no game. Here as the control — what every app on this floor is implicitly compared against.",
      prompt: "Review ten cards. Ask yourself what, if anything, would keep you coming back tomorrow.",
      url: "https://ankiweb.net", embed: false },
    { slug: "duolingo", kind: "museum", name: "Duolingo (Japanese)",
      blurb: "The mass-market path: streaks, leagues, bite-size lessons; kanji appear inside general Japanese lessons. A provocation about engagement mechanics vs kanji-specific teaching.",
      prompt: "Do one lesson. Count how often you produced a kanji versus merely tapped one.",
      url: "https://www.duolingo.com", embed: false }
  ],
  posterUrl: "",   // ✎ e.g. the session-1 materials hub (cards + sheet previews) — paste only if this audience should get it
  boardUrl:  "https://dpenl.github.io/kanjiWorkAdv/web/board.html",
  guideUrl:  "https://github.com/DpenL/kanjiWorkAdv/blob/main/docs/FLOOR-GUIDE.md"
};
var GUIDE = "Floor";
var STAMP_KEY = "kc_floor_stamps";
var FINISHERS = "kc_floor_finishers";

// ---- helpers ---------------------------------------------------------------
var visited = {};
var openP = null;
function say(m) { try { WA.chat.sendChatMessage(m, GUIDE); } catch (e) { console.log("[floor]", m); } }
function onEnter(layer, fn) { try { WA.room.onEnterLayer(layer).subscribe(fn); } catch (e) { console.warn("[floor]", layer, e); } }
function onLeave(layer, fn) { try { WA.room.onLeaveLayer(layer).subscribe(fn); } catch (e) { console.warn("[floor]", layer, e); } }
function closeP() { if (openP) { try { openP.close(); } catch (e) {} openP = null; } }
function popup(anchor, msg, buttons) {
  closeP();
  try { openP = WA.ui.openPopup(anchor, msg, buttons); }
  catch (e) { console.warn("[floor] popup", anchor, e); say(msg); }
}
function openUrl(url, embed) {
  if (embed) { try { WA.nav.openCoWebsite(url); return; } catch (e) { console.warn(e); } }
  try { WA.nav.openTab(url); } catch (e) { say(url); }
}
function count() { return Object.keys(visited).length; }
function total() { return CONFIG.stations.length; }
function persist() {
  try { WA.player.state.saveVariable(STAMP_KEY, JSON.stringify(visited), { public: false, persist: true, scope: "world" }); }
  catch (e) { try { WA.player.state[STAMP_KEY] = JSON.stringify(visited); } catch (e2) {} }
}
function progressLines() {
  return CONFIG.stations.map(function (s) {
    return (visited[s.slug] ? "✅ " : "⬜ ") + s.name;
  }).join("\n");
}
function refreshBtn() {
  try { WA.ui.actionBar.removeButton("floor-progress"); } catch (e) {}
  try {
    WA.ui.actionBar.addButton({ id: "floor-progress", label: "🎮 " + count() + "/" + total(),
      callback: function () { say("Stamp rally:\n" + progressLines()); } });
  } catch (e) { console.warn("[floor] actionBar", e); }
}
function stamp(s) {
  if (visited[s.slug]) return;
  visited[s.slug] = true; persist(); refreshBtn();
  say("📍 Stamp: " + s.name + " (" + count() + "/" + total() + ")");
  if (count() === total()) {
    bumpFinishers();
    say("🎉 All " + total() + " stamps! Walk to the 🏆 pedestal in the centre of the floor.");
  }
}
function bumpFinishers() {
  try {
    var n = parseInt(WA.state.loadVariable ? WA.state.loadVariable(FINISHERS) : WA.state[FINISHERS], 10) || 0;
    WA.state.saveVariable(FINISHERS, String(n + 1), { public: true, persist: true });
  } catch (e) { console.warn("[floor] finishers", e); }
}
function finishers() {
  try { return parseInt(WA.state.loadVariable ? WA.state.loadVariable(FINISHERS) : WA.state[FINISHERS], 10) || 0; }
  catch (e) { return 0; }
}

// ---- wiring -----------------------------------------------------------------
WA.onInit().then(function () {
  try {
    var saved = WA.player.state.loadVariable ? WA.player.state.loadVariable(STAMP_KEY) : WA.player.state[STAMP_KEY];
    if (saved) visited = JSON.parse(saved);
  } catch (e) {}
  refreshBtn();
  say("Welcome to the demo floor, online edition. 🕹 cabinets left (the kanji games), 🏛 museum wall right (the apps they get compared to). Stamp all " + total() + " stations, then visit the 🏆.");

  CONFIG.stations.forEach(function (s) {
    var zone = "zone_station_" + s.slug;
    onEnter(zone, function () {
      var txt = s.name + "\n" + (s.blurb || "This cabinet isn't wired to an online build yet — stamped visits still count.") + (s.prompt ? "\n\nTry: " + s.prompt : "");
      var buttons = [];
      if (s.url) {
        buttons.push({ label: "▶ Open", className: "primary", callback: function (p) { openUrl(s.url, s.embed); stamp(s); p.close(); } });
      } else {
        buttons.push({ label: "Stamp ✔", className: "primary", callback: function (p) { stamp(s); p.close(); } });
      }
      buttons.push({ label: "Later", className: "normal", callback: function (p) { p.close(); } });
      popup("popup_" + s.slug, txt, buttons);
    });
    onLeave(zone, closeP);
  });

  onEnter("zone_trophy", function () {
    var done = count() === total();
    var msg = done
      ? "🏆 Stamp rally complete — thanks for touring the whole floor!\nFinishers so far: " + (finishers() || "—") + "\nLeave a note on the 📌 board so the in-person crowd hears from you."
      : "Stamp rally: " + count() + "/" + total() + "\n\n" + progressLines();
    popup("popup_trophy", msg, [{ label: "OK", className: "normal", callback: function (p) { p.close(); } }]);
  });
  onLeave("zone_trophy", closeP);

  onEnter("zone_poster", function () {
    if (CONFIG.posterUrl) {
      popup("popup_poster", "The worlds poster and the session-1 card decks live here.", [
        { label: "▶ Open", className: "primary", callback: function (p) { openUrl(CONFIG.posterUrl, false); p.close(); } },
        { label: "Later", className: "normal", callback: function (p) { p.close(); } }]);
    } else {
      popup("popup_poster", "Poster wall — materials link not wired yet (CONFIG.posterUrl).", [
        { label: "OK", className: "normal", callback: function (p) { p.close(); } }]);
    }
  });
  onLeave("zone_poster", closeP);

  onEnter("zone_board", function () {
    popup("popup_board", "掲示板 — the common board. Leave a line: what you tried, what surprised you.", [
      { label: "▶ Open board", className: "primary", callback: function (p) { openUrl(CONFIG.boardUrl, false); p.close(); } },
      { label: "Later", className: "normal", callback: function (p) { p.close(); } }]);
  });
  onLeave("zone_board", closeP);

  onEnter("zone_cafe", function () { say("🍵 Floor café — step in to join the voice room."); });
}).catch(function (e) { console.error("WA init failed", e); });
