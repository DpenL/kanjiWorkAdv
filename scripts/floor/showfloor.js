/* Kanji Commons demo showfloor — minimal script, shared by study.tmj + arcade.tmj.
 * One interaction, identical at every booth: walk onto the pad -> one popup ->
 * the button opens the demo in a new browser tab. No quest UI, no extra chrome.
 * Roster: the publicly available session-1 demos + WaniKani + Anki.
 * (Own-game stands, stamp rally, voice tables etc. live in the backlog /
 * scripts/floor/theme.js from the decorated prototypes.) */

var STANDS = [
  { slug: "kanjicats", name: "Kanji Cats",
    url: "https://store.steampowered.com/app/3830660/Kanji_Cats_Demo/" },
  { slug: "nihongosdx", name: "Nihongo Showdown DX",
    url: "https://arbigaus.itch.io/nihongo-showdown-dx" },
  { slug: "bbv01", name: "Zen Hanzi",
    url: "https://saya1984.itch.io/bbv01" },
  { slug: "kanjistriker", name: "Kanji Striker",
    urls: [
      { label: "App Store", url: "https://apps.apple.com/us/app/kanji-striker/id6775400235" },
      { label: "Google Play", url: "https://play.google.com/store/apps/details?id=org.shimabird.kanjistriker" }
    ] },
  { slug: "wanikani", name: "WaniKani", url: "https://www.wanikani.com" },
  { slug: "anki", name: "Anki", url: "https://ankiweb.net" }
];

var openP = null;
function closeP() { if (openP) { try { openP.close(); } catch (e) {} openP = null; } }
function done(p) { try { p.close(); } catch (e) {} openP = null; }
function openTab(url) { try { WA.nav.openTab(url); } catch (e) { try { WA.chat.sendChatMessage(url, "Floor"); } catch (e2) {} } }
function host(url) { try { return url.split("/")[2].replace(/^www\./, ""); } catch (e) { return "the site"; } }

WA.onInit().then(function () {
  try {
    WA.chat.sendChatMessage("Welcome! Walk onto a booth's floor plate and press the button — every demo opens in a new browser tab.", "Floor");
  } catch (e) {}

  STANDS.forEach(function (s) {
    var zone = "zone_stand_" + s.slug;
    try {
      WA.room.onEnterLayer(zone).subscribe(function () {
        var buttons = [];
        var txt;
        if (s.urls) {
          txt = "【" + s.name + "】 Mobile app — the buttons open its store pages in a new tab.";
          s.urls.forEach(function (u) {
            buttons.push({ label: "▶ " + u.label, className: "primary",
              callback: function (p) { openTab(u.url); done(p); } });
          });
        } else {
          txt = "【" + s.name + "】 Opens " + host(s.url) + " in a new tab.";
          buttons.push({ label: "▶ Open", className: "primary",
            callback: function (p) { openTab(s.url); done(p); } });
        }
        closeP();
        try { openP = WA.ui.openPopup("popup_" + s.slug, txt, buttons); }
        catch (e) { console.warn("[floor]", zone, e); }
      });
      WA.room.onLeaveLayer(zone).subscribe(closeP);
    } catch (e) { console.warn("[floor]", zone, e); }
  });
}).catch(function (e) { console.error("WA init failed", e); });
