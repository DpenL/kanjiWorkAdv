/* KC Feature Lab — social room (topics 4, 5, 12).
 * T4 speed-dating ring: shared bubble + rotation timer (30 s demo; 4 min real).
 * T5 stage: jitsi zone + broadcast cue. True room-wide megaphone needs
 *   jitsiRoomAdminTag / speakerMegaphone — plan/hosting-gated, see review guide.
 * T12 role zones: player state + outline color = cheap "discipline-visible avatars". */

var DEMO_SECONDS = 30;
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Lab"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }

var timerRunning = false;
WA.onInit().then(function () {
  onEnter("zone_topic4_speeddate", function () {
    WA.ui.openPopup("speeddate", "T4 · Speed-dating ring. Pitch a mechanic to whoever shares the bubble. Start the rotation timer?", [
      { label: "Start (" + DEMO_SECONDS + "s demo)", className: "primary", callback: function (p) {
          if (!timerRunning) {
            timerRunning = true;
            say("⏱️ Timer started — " + DEMO_SECONDS + "s (would be 4 min at a real event).", "Moderator");
            setTimeout(function () {
              say("⏱️ Time! Rotate one ring to the right. (Broadcasting this to every ring is the Events-API test in ⑤ Collab.)", "Moderator");
              timerRunning = false;
            }, DEMO_SECONDS * 1000);
          }
          p.close();
        } },
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic5_stage", function () {
    say("🎙️ T5 · Stage: this jitsi zone joins everyone ON stage. True room-wide broadcast (megaphone) depends on speakerMegaphone/jitsiRoomAdminTag — verify on the hosted tier before promising keynotes.", "Stage");
    try { WA.camera.set(9 * 32, 3 * 32, 14 * 32, 8 * 32, false, true); } catch (e) { /* camera focus is a nice-to-have */ }
  });

  role("zone_topic12_role_developer", "DEV", [185, 198, 227]);
  role("zone_topic12_role_educator", "EDU", [168, 195, 160]);
  role("zone_topic12_role_researcher", "RES", [240, 199, 94]);
}).catch(function (e) { console.error("[lab social]", e); });

function role(zone, tag, rgb) {
  onEnter(zone, function () {
    try { WA.player.state.saveVariable("user_role", tag, { persist: true, public: true }); } catch (e) { try { WA.player.state.user_role = tag; } catch (e2) {} }
    try { WA.player.setOutlineColor(rgb[0], rgb[1], rgb[2]); } catch (e) {}
    say("You are tagged [" + tag + "] — outline recolored so roles are legible at a glance.", "Registrar");
  });
}
