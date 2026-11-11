/* Themed floor rooms (study.tmj + arcade.tmj) — shared script.
 * Same DEMOSTAND model as floor.js: every exhibit = device + poster popup +
 * walk-up pad + voice table (jitsi, SPACE). Both rooms carry the same booths
 * and slugs, so the stamp rally is one quest across both skins; the doors
 * between the rooms are the "skin toggle".
 *
 * Quest rule: a stamp is earned ONLY by actually opening a demo (▶ button).
 * Stands without an online build don't count toward the rally total.
 * Roster: session-1 publics (David, 11 Nov) + own games + industry references.
 */

// ---- config (edit me) -------------------------------------------------------
var CONFIG = {
  stands: [
    // own games (builds pending)
    { slug: "dragontale", name: "DragonTale",
      poster: "RPG for learning Japanese kanji, developed and iterated at TUM over several years.",
      prompt: "Play the opening minutes without help. Note the first moment the game teaches you a kanji — how does it do it?",
      url: "", embed: false },                                   // ✎ web build URL when one exists
    { slug: "radfighters", name: "Radical Fighters",
      poster: "",                                                 // ✎ David's one-liner (PoC on the KanKyouKen platform)
      prompt: "Play one round. Watch what the game seems to notice about you while you play.",
      url: "", embed: false },                                   // ✎ build URL
    { slug: "majikana", name: "Music to My Ears / Maji Kana",
      poster: "",                                                 // ✎ confirm build availability (as on the physical floor)
      prompt: "",
      url: "", embed: false },                                   // ✎ build URL
    // public demos shown at session 1 (links from David, 11 Nov)
    { slug: "kanjicats", name: "Kanji Cats",
      poster: "Playable demo on Steam — ▶ opens the store page (play via Steam).",
      prompt: "",
      url: "https://store.steampowered.com/app/3830660/Kanji_Cats_Demo/", embed: true },
    { slug: "nihongosdx", name: "Nihongo Showdown DX",
      poster: "Build on itch.io — ▶ opens the game page.",
      prompt: "",
      url: "https://arbigaus.itch.io/nihongo-showdown-dx", embed: false },
    { slug: "bbv01", name: "bbv01",
      poster: "Build on itch.io — ▶ opens the game page.",
      prompt: "",
      url: "https://saya1984.itch.io/bbv01", embed: false },
    { slug: "kanjistriker", name: "Kanji Striker",
      poster: "Mobile app — pick your store; either click counts as trying it.",
      prompt: "",
      urls: [
        { label: "App Store", url: "https://apps.apple.com/us/app/kanji-striker/id6775400235" },
        { label: "Google Play", url: "https://play.google.com/store/apps/details?id=org.shimabird.kanjistriker" }
      ], embed: false },
    // industry references (look-and-compare; links open in a new tab)
    { slug: "wanikani", name: "WaniKani",
      poster: "Commercial web app: spaced repetition for ~2,000 kanji and ~6,000 words, taught through mnemonics and levels. Not a game in the play sense — a provocation about what “gamified” means.",
      prompt: "Do a few review items. Notice what it does when you get one wrong — and how that feels.",
      url: "https://www.wanikani.com", embed: false },
    { slug: "anki", name: "Anki (plain deck)",
      poster: "The baseline: a free SRS flashcard app with a community kanji deck. Pure repetition, no game. Here as the control — what every app on this floor is implicitly compared against.",
      prompt: "Review ten cards. Ask yourself what, if anything, would keep you coming back tomorrow.",
      url: "https://ankiweb.net", embed: false },
    { slug: "duolingo", name: "Duolingo (Japanese)",
      poster: "The mass-market path: streaks, leagues, bite-size lessons; kanji appear inside general Japanese lessons. A provocation about engagement mechanics vs kanji-specific teaching.",
      prompt: "Do one lesson. Count how often you produced a kanji versus merely tapped one.",
      url: "https://www.duolingo.com", embed: false }
  ],
  posterUrl: "",    // ✎ e.g. the session-1 materials hub — paste only if this audience should get it
  boardUrl:  "https://dpenl.github.io/kanjiWorkAdv/web/board.html",
  feedbackUrl: "",  // ✎ async feedback form/page; when set, stands get a 💬 button + exit nudge
  guideUrl:  "https://github.com/DpenL/kanjiWorkAdv/blob/main/docs/FLOOR-GUIDE.md"
};
var GUIDE = "Floor";
var STAMP_KEY = "kc_floor_stamps";
var FINISHERS = "kc_floor_finishers";

// ---- helpers ---------------------------------------------------------------
var visited = {};
var openP = null;
var lastCafe = 0;
var nudged = false;
function say(m) { try { WA.chat.sendChatMessage(m, GUIDE); } catch (e) { console.log("[floor]", m); } }
function onEnter(layer, fn) { try { WA.room.onEnterLayer(layer).subscribe(fn); } catch (e) { console.warn("[floor]", layer, e); } }
function onLeave(layer, fn) { try { WA.room.onLeaveLayer(layer).subscribe(fn); } catch (e) { console.warn("[floor]", layer, e); } }
function closeP() { if (openP) { try { openP.close(); } catch (e) {} openP = null; } }
function done(p) { try { p.close(); } catch (e) {} openP = null; }
function popup(anchor, msg, buttons) {
  closeP();
  try { openP = WA.ui.openPopup(anchor, msg, buttons); }
  catch (e) { console.warn("[floor] popup", anchor, e); say(msg); }
}
function openUrl(url, embed) {
  if (embed) { try { WA.nav.openCoWebsite(url); return; } catch (e) { console.warn(e); } }
  try { WA.nav.openTab(url); } catch (e) { say(url); }
}
function feedbackUrlFor(slug) {
  var u = CONFIG.feedbackUrl;
  return u + (u.indexOf("?") >= 0 ? "&" : "?") + "stand=" + slug;
}
// quest: only stands with a real URL count ("stamp = you actually opened it")
function isWired(s) { return !!s.url || (s.urls && s.urls.length > 0); }
function wired() { return CONFIG.stands.filter(isWired); }
function total() { return wired().length; }
function count() { return wired().filter(function (s) { return visited[s.slug]; }).length; }
function persist() {
  try { WA.player.state.saveVariable(STAMP_KEY, JSON.stringify(visited), { public: false, persist: true, scope: "world" }); }
  catch (e) { try { WA.player.state[STAMP_KEY] = JSON.stringify(visited); } catch (e2) {} }
}
function bulletList() {
  return CONFIG.stands.map(function (s) {
    if (!isWired(s)) return "• 🔧 " + s.name + " (coming soon)";
    return "• " + (visited[s.slug] ? "✅ " : "⬜ ") + s.name;
  }).join("\n");
}
function missingNames() {
  return wired().filter(function (s) { return !visited[s.slug]; })
    .map(function (s) { return s.name; }).join(", ");
}
function refreshBtn() {
  try { WA.ui.actionBar.removeButton("floor-progress"); } catch (e) {}
  try {
    WA.ui.actionBar.addButton({ id: "floor-progress", label: "🎮 " + count() + "/" + total(),
      callback: function () { say("Stamp rally " + count() + "/" + total() + "\n" + bulletList()); } });
  } catch (e) { console.warn("[floor] actionBar", e); }
}
function stamp(s) {
  if (!isWired(s) || visited[s.slug]) return;
  visited[s.slug] = true; persist(); refreshBtn();
  say("📍 Stamp: " + s.name + " (" + count() + "/" + total() + ")");
  if (count() === total() && total() > 0) {
    bumpFinishers();
    say("🎉 " + total() + "/" + total() + " — you've tried everything that's online so far. The 🏆 shrine salutes you; leave a line on the 📌 board!");
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
  say("Welcome to Kanji Commons. Every stand is a booth + a demo: walk up, read, ▶ open it — that's what earns the stamp. The door between the study hall and the arcade keeps your progress.");
  if (total() > 0) {
    say("Stamp rally " + count() + "/" + total() + " — track it with the 🎮 button in the top bar.\n" + bulletList());
  }

  CONFIG.stands.forEach(function (s) {
    var zone = "zone_stand_" + s.slug;
    onEnter(zone, function () {
      var txt = "【" + s.name + "】 " + (s.poster || "");
      if (s.prompt) txt += "  ▶ Try: " + s.prompt;
      var buttons = [];
      if (s.urls && s.urls.length) {
        s.urls.forEach(function (u) {
          buttons.push({ label: "▶ " + u.label, className: "primary",
            callback: function (p) { openUrl(u.url, false); stamp(s); done(p); } });
        });
        buttons.push({ label: "Later", className: "normal", callback: function (p) { done(p); } });
      } else if (s.url) {
        buttons.push({ label: "▶ Open", className: "primary", callback: function (p) { openUrl(s.url, s.embed); stamp(s); done(p); } });
        buttons.push({ label: "Later", className: "normal", callback: function (p) { done(p); } });
      } else {
        txt += "  (⏳ online build coming soon — doesn't count toward the rally yet.)";
        buttons.push({ label: "OK", className: "normal", callback: function (p) { done(p); } });
      }
      if (CONFIG.feedbackUrl && isWired(s)) {
        buttons.push({ label: "💬", className: "normal",
          callback: function (p) { openUrl(feedbackUrlFor(s.slug), false); done(p); } });
      }
      popup("popup_" + s.slug, txt, buttons);
    });
    onLeave(zone, closeP);
  });

  onEnter("zone_trophy", function () {
    var c = count(), t = total();
    var complete = t > 0 && c === t;
    var msg = complete
      ? "🏆 " + c + "/" + t + " — you've tried everything that's online so far! Finishers: " + (finishers() || "—") + ". Leave a line on the 📌 board so the in-person crowd hears from you."
      : "🏆 スタンプラリー " + c + "/" + t + (t > 0 ? " — missing: " + missingNames() : "");
    popup("popup_trophy", msg, [
      { label: "List", className: "normal", callback: function (p) { say("Stamp rally " + c + "/" + t + "\n" + bulletList()); done(p); } },
      { label: "OK", className: "primary", callback: function (p) { done(p); } }]);
  });
  onLeave("zone_trophy", closeP);

  onEnter("zone_poster", function () {
    if (CONFIG.posterUrl) {
      popup("popup_poster", "The worlds poster and the session-1 card decks live here.", [
        { label: "▶ Open", className: "primary", callback: function (p) { openUrl(CONFIG.posterUrl, false); done(p); } },
        { label: "Later", className: "normal", callback: function (p) { done(p); } }]);
    } else {
      popup("popup_poster", "Poster wall — materials link not wired yet (CONFIG.posterUrl).", [
        { label: "OK", className: "normal", callback: function (p) { done(p); } }]);
    }
  });
  onLeave("zone_poster", closeP);

  onEnter("zone_board", function () {
    popup("popup_board", "掲示板 — the common board. Leave a line: what you tried, what surprised you.", [
      { label: "▶ Open board", className: "primary", callback: function (p) { openUrl(CONFIG.boardUrl, false); done(p); } },
      { label: "Later", className: "normal", callback: function (p) { done(p); } }]);
  });
  onLeave("zone_board", closeP);

  onEnter("zone_cafe", function () {
    var now = Date.now();
    if (now - lastCafe > 60000) { lastCafe = now; say("🍵 Step closer to join the voice table."); }
  });

  // async feedback nudge at the exits (only when a feedback target is wired)
  ["exit-genkan", "exit-study", "exit-arcade"].forEach(function (z) {
    onEnter(z, function () {
      if (CONFIG.feedbackUrl && !nudged && count() > 0) {
        nudged = true;
        say("💬 One line before you go? " + CONFIG.feedbackUrl);
      }
    });
  });
}).catch(function (e) { console.error("WA init failed", e); });
