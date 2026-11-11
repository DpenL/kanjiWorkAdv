/* KC Feature Lab — data-kiosk room (topics 8, 9, 11).
 * T8 live kanjiapi.dev fetch (the CORS/live-API feasibility test).
 * T9 KanjiVG twice on purpose: script-driven embed vs map-property embed —
 *   same feature, two mechanisms, pick one after review.
 * T11 genre museum: embeddable (kanji.garden) vs non-embeddable (Influent)
 *   vs academic graveyard (TUM Dragon Tale) — three exhibit patterns. */

var KANJI = ["学", "字", "猫", "漢", "語", "遊"];
var siteHandle;
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Kiosk"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function onLeave(l, fn) { try { WA.room.onLeaveLayer(l).subscribe(fn); } catch (e) {} }
function openSite(url, big) {
  try {
    return WA.ui.website.open({ url: url, allowApi: false,
      position: { vertical: "middle", horizontal: big ? "middle" : "right" },
      size: big ? { height: "85vh", width: "80vw" } : { height: "100vh", width: "420px" } });
  } catch (e) { try { WA.nav.openCoWebSite(url); } catch (e2) { say("Open manually: " + url); } }
}
function closeSite() { if (siteHandle && siteHandle.then) { siteHandle.then(function (w) { try { w.close(); } catch (e) {} }); } siteHandle = null; }

WA.onInit().then(function () {
  onEnter("zone_topic8_api", function () {
    var k = KANJI[Math.floor(Math.random() * KANJI.length)];
    say("Querying kanjiapi.dev for 「" + k + "」…");
    fetch("https://kanjiapi.dev/v1/kanji/" + encodeURIComponent(k))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        say("「" + k + "」 " + (d.meanings || []).join(", ") + " · " + (d.kun_readings || []).slice(0, 2).join("・") +
            (d.jlpt ? " · JLPT N" + d.jlpt : "") + " · " + d.stroke_count + " strokes  (live KANJIDIC2 data — CC BY-SA, EDRDG)", "API");
      })
      .catch(function () { say("kanjiapi.dev unreachable from the script sandbox — that itself is a finding; note it in the guide.", "API"); });
  });

  onEnter("zone_topic9_tracing", function () {
    say("T9 · Script-driven embed of the local KanjiVG kiosk (compare with the map-property booth next door).");
    siteHandle = openSite("../../web/tracing.html", false);
  });
  onLeave("zone_topic9_tracing", closeSite);

  onEnter("zone_topic11_kanjigarden", function () {
    say("T11 · Trying to iframe kanji.garden — if the panel stays blank it sends X-Frame-Options and we exhibit via link instead. Either result is the test outcome.");
    siteHandle = openSite("https://kanji.garden", true);
  });
  onLeave("zone_topic11_kanjigarden", closeSite);

  onEnter("zone_topic11_influent", function () {
    WA.ui.openPopup("influent", "T11 · Influent (Steam, 3D vocab world) — desktop-only, can't embed. Museum pattern: trailer + design post-mortem on a panel.", [
      { label: "Steam page", className: "primary", callback: function (p) { try { WA.nav.openTab("https://store.steampowered.com/app/274980/Influent/"); } catch (e) {} p.close(); } },
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic11_graveyard", function () {
    WA.ui.openPopup("graveyard",
      "T11 · Academic graveyard: prototypes that never shipped — e.g. TUM's Dragon Tale (AR stroke-order quests). Exhibit the THESES and the reasons they stalled; that is the research-positioning content.", [
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });
}).catch(function (e) { console.error("[lab data]", e); });
