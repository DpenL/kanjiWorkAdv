/* KC Feature Lab — pedagogy room (topics 6, 10, 19).
 * T6 cognitive-load testbench + radical-decomposition lab (opt-in popups).
 * T10 Leitner boxes: five walkable strips; your card's box PERSISTS in player
 *   state across sessions — the spatial-SRS demo. FSRS sandbox stays queued.
 * T19 evaluation matrix: the educator-facing quality gate as a popup. */

var CARD = { word: "猫", meaning: "cat" };
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Lab"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function getBox() { try { return parseInt(WA.player.state.kc_lab_leitner, 10) || 1; } catch (e) { return 1; } }
function setBox(n) { try { WA.player.state.saveVariable("kc_lab_leitner", n, { persist: true }); } catch (e) { try { WA.player.state.kc_lab_leitner = n; } catch (e2) {} } }

WA.onInit().then(function () {
  onEnter("zone_topic6_cogload", function () {
    WA.ui.openPopup("cogload",
      "T6 · Cognitive-load check (Sweller): does your mechanic test MEMORY & composition (germane load) or REFLEXES & timing (extraneous load)? Kanji games fail when speed pressure crowds out encoding.", [
      { label: "Noted", className: "primary", callback: function (p) { p.close(); } }
    ]);
  });

  onEnter("zone_topic6_radical_lab", function () {
    WA.ui.openPopup("radical",
      "T6 · Decomposition: 漢 = 氵water + 堇 clay · 字 = 宀 roof + 子 child.\nMechanic seed: creatures/parts per radical (→ RadicalFighters). Data: RADKFILE/KRADFILE, IDS.", [
      { label: "Open kanji kiosk", className: "primary", callback: function (p) { try { WA.nav.openCoWebSite("../../web/kanji-quiz.html"); } catch (e) { say("Kiosk: web/kanji-quiz.html"); } p.close(); } },
      { label: "Close", className: "normal", callback: function (p) { p.close(); } }
    ]);
  });

  for (var i = 1; i <= 5; i++) leitner(i);

  onEnter("zone_topic19_eval_matrix", function () {
    WA.ui.openPopup("evalmatrix",
      "T19 · Pedagogy gate: (1) Does it teach components, not arbitrary pictures? (2) Is recall active, not recognition-only? (3) Could a teacher run it in one class hour?", [
      { label: "Passes", className: "success", callback: function (p) { say("Self-assessed: passes the matrix. Log it on the board in ⑥.", "Eval"); p.close(); } },
      { label: "Needs redesign", className: "error", callback: function (p) { say("Honest answer — park it in the wiki with what failed.", "Eval"); p.close(); } }
    ]);
  });
}).catch(function (e) { console.error("[lab pedagogy]", e); });

function leitner(n) {
  onEnter("zone_topic10_leitner_box" + n, function () {
    var box = getBox();
    if (n !== box) { say("T10 · Box " + n + ". Your card 「" + CARD.word + "」 currently lives in box " + box + " — walk there to review it.", "SRS"); return; }
    WA.ui.openPopup("leitner" + n, "T10 · Box " + n + " review: what does 「" + CARD.word + "」 mean?", [
      { label: "Knew it (" + CARD.meaning + ")", className: "success", callback: function (p) {
          setBox(Math.min(n + 1, 5)); say("→ promoted to box " + Math.min(n + 1, 5) + ". This persists across sessions (player state).", "SRS"); p.close(); } },
      { label: "Forgot", className: "error", callback: function (p) {
          setBox(1); say("→ back to box 1. Spaced repetition, walked.", "SRS"); p.close(); } }
    ]);
  });
}
