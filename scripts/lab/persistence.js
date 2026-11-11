/* KC Feature Lab — persistence room (topics 17, 18, 20).
 * T17 vote tiles on ROOM state (shared across players, live) + reset desk.
 * T18 message pillar: a note that outlives sessions. Free-text entry needs a
 *   UIWebsite input page — popup mock here, upgrade path in the guide.
 * T20 trophy room + tie-in to the existing web/board.html ema wall (map-prop zone). */

function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Lab"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function getN(k) { try { return parseInt(WA.state[k], 10) || 0; } catch (e) { return 0; } }
function setS(k, v) { try { WA.state.saveVariable(k, v); } catch (e) { try { WA.state[k] = v; } catch (e2) {} } }

WA.onInit().then(function () {
  onEnter("zone_topic17_vote_green", function () {
    setS("kc_votes_green", getN("kc_votes_green") + 1);
    say("🟢 'Works for me' — tally " + getN("kc_votes_green") + " green / " + getN("kc_votes_red") + " red. Open a second browser window: the tally is SHARED room state.", "Poll");
  });
  onEnter("zone_topic17_vote_red", function () {
    setS("kc_votes_red", getN("kc_votes_red") + 1);
    say("🔴 'Confusing' — tally " + getN("kc_votes_green") + " green / " + getN("kc_votes_red") + " red.", "Poll");
  });
  onEnter("zone_topic17_vote_reset", function () {
    WA.ui.openPopup("voteReset", "Reset the shared tallies (" + getN("kc_votes_green") + "🟢/" + getN("kc_votes_red") + "🔴)?", [
      { label: "Reset", className: "error", callback: function (p) { setS("kc_votes_green", 0); setS("kc_votes_red", 0); say("Tallies reset for everyone.", "Poll"); p.close(); } },
      { label: "Keep", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic18_message_pillar", function () {
    var msg = "";
    try { msg = WA.state.kc_pillar || ""; } catch (e) {}
    WA.ui.openPopup("pillar", "T18 · Pillar message:\n「" + (msg || "still blank — be the first") + "」\nLeave your mark? (Free text needs a UIWebsite form — this demo stamps name+time.)", [
      { label: "Stamp it", className: "primary", callback: function (p) {
          var stamp = (WA.player.name || "anonymous") + " was here · " + new Date().toISOString().slice(0, 16).replace("T", " ");
          setS("kc_pillar", stamp);
          say("Pillar now reads: 「" + stamp + "」 — log out and back in: it persists.", "Pillar");
          p.close();
        } },
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic20_trophy", function () {
    WA.ui.openPopup("trophy",
      "T20 · Trophy room: permanent pedestals for finished community projects (name, team, one design lesson, repo link). Empty by design until the first event — history accumulates here.", [
      { label: "Example: repo", className: "primary", callback: function (p) { try { WA.nav.openTab("https://github.com/DpenL/kanjiWorkAdv"); } catch (e) {} p.close(); } },
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });
}).catch(function (e) { console.error("[lab persistence]", e); });
