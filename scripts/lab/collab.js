/* KC Feature Lab — collaboration room (topics 7, 13, 15).
 * T7 Etherpad sidebar + live GitHub commits terminal (repo activity in-world).
 * T13 standup circle (jitsi + shared pad) and the sprint bell — the Events-API
 *   test: one player rings, EVERY player in the room hears it (radio-taisō!).
 * T15 Excalidraw big-modal whiteboard. */

var CONFIG = {
  pad:        "https://etherpad.wikimedia.org/p/kanji-commons-lab",
  standupPad: "https://etherpad.wikimedia.org/p/kanji-commons-standup",
  repo:       "DpenL/kanjiWorkAdv"   // owner/name for the commits terminal
};
var siteHandle;
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Lab"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function onLeave(l, fn) { try { WA.room.onLeaveLayer(l).subscribe(fn); } catch (e) {} }
function sidebar(url) {
  try { return WA.ui.website.open({ url: url, position: { vertical: "top", horizontal: "right" }, size: { height: "100vh", width: "420px" } }); }
  catch (e) { try { WA.nav.openCoWebSite(url); } catch (e2) { say("Open manually: " + url); } }
}
function closeSite() { if (siteHandle && siteHandle.then) { siteHandle.then(function (w) { try { w.close(); } catch (e) {} }); } siteHandle = null; }

WA.onInit().then(function () {
  onEnter("zone_topic7_etherpad", function () { say("T7 · Shared pad — survives everyone leaving. Wiki remains the source of truth; pads are scratch."); siteHandle = sidebar(CONFIG.pad); });
  onLeave("zone_topic7_etherpad", closeSite);

  onEnter("zone_topic7_github_terminal", function () {
    say("Fetching last commits of " + CONFIG.repo + "…", "GitHub");
    fetch("https://api.github.com/repos/" + CONFIG.repo + "/commits?per_page=3")
      .then(function (r) { return r.json(); })
      .then(function (cs) {
        if (!cs.map) { say("GitHub API said: " + (cs.message || "unexpected reply"), "GitHub"); return; }
        cs.forEach(function (c) {
          say("· " + c.sha.slice(0, 7) + " " + (c.commit.message || "").split("\n")[0].slice(0, 70) + " — " + c.commit.author.name, "GitHub");
        });
      })
      .catch(function () { say("GitHub unreachable from sandbox — note as finding.", "GitHub"); });
  });

  onEnter("zone_topic13_standup", function () {
    say("T13 · Standup circle: voice bubble + shared pad. Type yesterday/today/blockers.", "Agile");
    siteHandle = sidebar(CONFIG.standupPad);
    try { WA.event.broadcast("kc-standup-join", { name: WA.player.name }); } catch (e) {}
  });
  onLeave("zone_topic13_standup", closeSite);

  onEnter("zone_topic13_sprint_bell", function () {
    WA.ui.openPopup("bell", "T13 · Sprint bell / radio-taisō: broadcast a bell to EVERY player in the room right now?", [
      { label: "Ring 🔔", className: "primary", callback: function (p) {
          try { WA.event.broadcast("kc-bell", { by: WA.player.name || "someone" }); say("Rung — check other browser windows.", "Bell"); }
          catch (e) { say("Events API unavailable on this version — finding for the guide.", "Bell"); }
          p.close();
        } },
      { label: "Cancel", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  try {
    WA.event.on("kc-bell").subscribe(function (ev) {
      say("🔔🧘 " + ((ev.data && ev.data.by) || "Someone") + " rings the bell — stand up, stretch, 30 seconds. (Broadcast received via Events API.)", "Bell");
    });
    WA.event.on("kc-standup-join").subscribe(function (ev) {
      say(((ev.data && ev.data.name) || "Someone") + " joined the standup circle.", "Agile");
    });
  } catch (e) { console.warn("[lab] events api", e); }

  onEnter("zone_topic15_excalidraw", function () { say("T15 · Shared whiteboard (Excalidraw iframes cleanly). For persistence use a fixed room URL."); siteHandle = openBig("https://excalidraw.com/"); });
  onLeave("zone_topic15_excalidraw", closeSite);
}).catch(function (e) { console.error("[lab collab]", e); });

function openBig(url) {
  try { return WA.ui.website.open({ url: url, position: { vertical: "middle", horizontal: "middle" }, size: { height: "85vh", width: "80vw" } }); }
  catch (e) { try { WA.nav.openCoWebSite(url); } catch (e2) { say("Open manually: " + url); } }
}
