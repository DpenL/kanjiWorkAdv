/* Kanji Commons — Genkan (entry/tutorial) map script.
 * Plain-JS WorkAdventure script (map property "script"). No build step needed.
 * NOTE: the WA scripting API evolves; every call is wrapped defensively so an
 * API change degrades gracefully instead of breaking the room.
 */

// ---- config (edit me) -------------------------------------------------------
var DISCORD_HELP_WEBHOOK = ""; // paste a Discord webhook URL to enable the Help Bell
var GUIDE = "Genkan Guide";

// ---- tiny i18n --------------------------------------------------------------
var STR = {
  en: {
    welcome: "Welcome to Kanji Commons! Walk with arrow keys or WASD. Step on a flag tile to choose your language.",
    lang: "Language set to English. Next: step into the green circle to try a voice bubble.",
    bubble: "You are in a conversation circle — anyone standing here can hear each other. Step out to leave it.",
    exit: "When you're ready, walk through the red torii on the right to enter the commons. 行ってらっしゃい!",
    help_sent: "Help requested — a greeter has been pinged and will come to you.",
    help_off: "Help bell not wired up yet. Ask in chat, or see the board in the commons."
  },
  ja: {
    welcome: "Kanji Commonsへようこそ！矢印キーかWASDで歩けます。旗のタイルに乗って言語を選んでください。",
    lang: "言語を日本語に設定しました。次は緑の円に入って、ボイスバブルを試してみましょう。",
    bubble: "会話サークルの中です。ここに立っている人同士で話せます。出ると会話も終わります。",
    exit: "準備ができたら、右の赤い鳥居をくぐってコモンズへどうぞ。",
    help_sent: "ヘルプを呼びました。案内係がすぐに来ます。",
    help_off: "ヘルプベルは未設定です。チャットで聞くか、コモンズの掲示板をご覧ください。"
  }
};
var lang = "en";
function t(k){ return (STR[lang] && STR[lang][k]) || STR.en[k]; }
function say(msg){ try { WA.chat.sendChatMessage(msg, GUIDE); } catch(e) { console.log("[genkan]", msg); } }
function onEnter(layer, fn){ try { WA.room.onEnterLayer(layer).subscribe(fn); } catch(e) { console.warn("onEnterLayer failed:", layer, e); } }

WA.onInit().then(function () {
  say(t("welcome"));

  onEnter("zone/lang-en", function(){ lang = "en"; persistLang(); say(t("lang")); });
  onEnter("zone/lang-ja", function(){ lang = "ja"; persistLang(); say(t("lang")); });
  onEnter("zone/bubble-demo", function(){ say(t("bubble")); say(t("exit")); });

  // Help Bell — one persistent button, escalates to Discord if configured.
  try {
    WA.ui.actionBar.addButton({
      id: "help-bell",
      label: "🔔 Help",
      callback: function(){
        if (DISCORD_HELP_WEBHOOK) {
          fetch(DISCORD_HELP_WEBHOOK, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: "🔔 Help requested in the Genkan (entry room)." })
          }).then(function(){ say(t("help_sent")); })
            .catch(function(){ say(t("help_off")); });
        } else { say(t("help_off")); }
      }
    });
  } catch(e) { console.warn("actionBar unavailable in this WA version", e); }
}).catch(function(e){ console.error("WA init failed", e); });

function persistLang(){
  try { WA.player.state.saveVariable("kc_lang", lang, { public: false, persist: true, scope: "world" }); }
  catch(e) { try { WA.player.state.kc_lang = lang; } catch(e2) { /* older API */ } }
}
