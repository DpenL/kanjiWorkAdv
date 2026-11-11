/* KC Feature Lab — onboarding room (topics 1–3).
 * T1 airlock: spawn cage whose barrier layer hides (and stops colliding) after
 *   an explicit "I understand" click — the anti-lost pattern, opt-in flavor.
 * T2 audio circle: labeled proximity/jitsi ring to teach voice bubbles.
 * T3 language tiles: set language state used by later popups. */

var airlockPopup;
var STR = {
  en: { unlocked: "Door unlocked — follow the lantern path. Nothing here is timed.",
        lang: "Language set to English. Popups will prefer English." },
  ja: { unlocked: "ドアが開きました。ランタンの道を進んでください。",
        lang: "言語を日本語に設定しました。" }
};
function lang() { try { return WA.player.state.kc_lang || "en"; } catch (e) { return "en"; } }
function say(m, who) { try { WA.chat.sendChatMessage(m, who || "Genkan-sensei"); } catch (e) { console.log("[lab]", m); } }
function onEnter(l, fn) { try { WA.room.onEnterLayer(l).subscribe(fn); } catch (e) { console.warn("[lab]", l, e); } }
function onLeave(l, fn) { try { WA.room.onLeaveLayer(l).subscribe(fn); } catch (e) {} }

WA.onInit().then(function () {
  onEnter("zone_topic1_airlock", function () {
    airlockPopup = WA.ui.openPopup("airlock",
      "T1 · The Airlock. Move with WASD/arrows. Click when ready — the barrier opens and stays open.", [
      { label: "I understand — unlock", className: "success", callback: function (p) {
          try { WA.room.hideLayer("barrier_topic1_airlock"); } catch (e) { console.warn(e); }
          say(STR[lang()].unlocked);
          p.close();
        } }
    ]);
  });
  onLeave("zone_topic1_airlock", function () { if (airlockPopup) { try { airlockPopup.close(); } catch (e) {} } });

  onEnter("zone_topic2_audiocircle", function () {
    say("T2 · You are in a conversation ring: anyone standing here shares a voice bubble. Step out to leave it.");
  });

  onEnter("zone_topic3_flag_en", function () {
    try { WA.player.state.saveVariable("kc_lang", "en", { persist: true }); } catch (e) { try { WA.player.state.kc_lang = "en"; } catch (e2) {} }
    say(STR.en.lang, "System");
  });
  onEnter("zone_topic3_flag_jp", function () {
    try { WA.player.state.saveVariable("kc_lang", "ja", { persist: true }); } catch (e) { try { WA.player.state.kc_lang = "ja"; } catch (e2) {} }
    say(STR.ja.lang, "System");
  });
}).catch(function (e) { console.error("[lab onboarding]", e); });
