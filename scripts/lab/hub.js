/* KC Feature Lab — hub. Carries the "virtual smartphone" overlay (persistent
 * action-bar menu) so it can be reviewed against the zone-based alternatives.
 * Everything degrades gracefully when CONFIG is empty. */

var CONFIG = {
  wiki:      "https://github.com/DpenL/kanjiWorkAdv/wiki",   // knowledge base / source of truth
  calendar:  "",   // e.g. https://calendar.google.com/calendar/embed?src=<public-id>
  helpHook:  "",   // Discord webhook URL for the Help Bell
  guide:     "https://github.com/DpenL/kanjiWorkAdv/blob/main/docs/LAB-REVIEW-GUIDE.md"
};

function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Lab"); } catch (e) { console.log("[lab]", m); } }
function onEnter(layer, fn) { try { WA.room.onEnterLayer(layer).subscribe(fn); } catch (e) { console.warn("[lab]", layer, e); } }

function menu(label, fn) { try { WA.ui.registerMenuCommand(label, fn); } catch (e) { console.warn("[lab] menu", label, e); } }

WA.onInit().then(function () {
  say("Welcome to the Feature Lab hub. Each door tests one feature cluster — see the review guide (menu ▸ 🗺).");

  // ---- Virtual smartphone (Gemini module, reimplemented; test subject itself) ----
  menu("📅 Event calendar", function () {
    if (!CONFIG.calendar) { say("Calendar not wired yet — set CONFIG.calendar in scripts/lab/hub.js"); return; }
    try { WA.ui.website.open({ url: CONFIG.calendar, position: { vertical: "top", horizontal: "right" }, size: { height: "100vh", width: "400px" } }); }
    catch (e) { try { WA.nav.openTab(CONFIG.calendar); } catch (e2) { say(CONFIG.calendar); } }
  });
  menu("📚 Resource wiki", function () {
    try { WA.nav.openTab(CONFIG.wiki); } catch (e) { say(CONFIG.wiki); }
  });
  menu("🔔 Call for help", function () {
    WA.ui.openPopup("hubHelp", "Ping a human helper on Discord?", [
      { label: "Send", className: "error", callback: function (p) {
          if (CONFIG.helpHook) {
            fetch(CONFIG.helpHook, { method: "POST", headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ content: "🔔 " + (WA.player.name || "Someone") + " asks for help in the Feature Lab hub" }) })
              .then(function () { say("Help request sent — someone will come to you."); })
              .catch(function () { say("Webhook failed — check CONFIG.helpHook."); });
          } else { say("Help Bell not wired yet (CONFIG.helpHook empty) — this popup is the dry run."); }
          p.close();
        } },
      { label: "Cancel", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });
  menu("🏷️ Set my discipline", function () {
    WA.ui.openPopup("hubRole", "Your primary hat today?", [
      { label: "DEV", className: "primary", callback: function (p) { setRole("DEV", "#B9C6E3"); p.close(); } },
      { label: "EDU", className: "primary", callback: function (p) { setRole("EDU", "#A8C3A0"); p.close(); } },
      { label: "RES", className: "primary", callback: function (p) { setRole("RES", "#F0C75E"); p.close(); } }
    ]);
  });
  menu("🗺️ Lab review guide", function () { try { WA.nav.openTab(CONFIG.guide); } catch (e) { say(CONFIG.guide); } });

  onEnter("zone_welcome", function () {
    say("Doors: ① onboarding ② social ③ pedagogy ④ data ⑤ collab ⑥ persistence ⑦ integrations. Bottom-left torii returns to the genkan.");
  });
}).catch(function (e) { console.error("[lab hub]", e); });

function setRole(role, color) {
  try { WA.player.state.saveVariable("user_role", role, { persist: true, public: true }); } catch (e) { try { WA.player.state.user_role = role; } catch (e2) {} }
  try { WA.player.setOutlineColor(parseInt(color.slice(1, 3), 16), parseInt(color.slice(3, 5), 16), parseInt(color.slice(5, 7), 16)); } catch (e) {}
  say("Tagged as [" + role + "] — outline color set so others can read your role.");
}
