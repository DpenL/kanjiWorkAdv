/* Kanji Commons — main commons map script.
 * Features: zone hints, "virtual smartphone lite" (action-bar buttons), and an
 * opt-in stamp rally (スタンプラリー) across the four rooms. All opt-in — no
 * locked doors, no forced tutorials.
 */

// ---- config (edit me) -------------------------------------------------------
var LINKS = {
  wiki:     "",   // e.g. your GitHub wiki / Notion — persistent source of truth
  discord:  "",   // invite link — async backbone
  schedule: "",   // event schedule page (can be a wiki page)
  helpHook: ""    // Discord webhook for the Help Bell
};
var GUIDE = "Commons";
var STAMPS = ["zone/stage","zone/breakout","zone/library","zone/karaoke"];
var STAMP_NAMES = { "zone/stage":"Stage 舞台","zone/breakout":"Breakout 座敷","zone/library":"Library 図書室","zone/karaoke":"Karaoke カラオケ" };

var visited = {};
function say(m){ try { WA.chat.sendChatMessage(m, GUIDE); } catch(e){ console.log("[commons]", m); } }
function onEnter(layer, fn){ try { WA.room.onEnterLayer(layer).subscribe(fn); } catch(e){ console.warn(e); } }
function openTab(url, fallbackMsg){
  if (!url) { say(fallbackMsg); return; }
  try { WA.nav.openTab(url); } catch(e) { say(url); }
}

WA.onInit().then(function () {
  // restore stamp progress
  try {
    var saved = WA.player.state.loadVariable ? WA.player.state.loadVariable("kc_stamps") : WA.player.state.kc_stamps;
    if (saved) visited = JSON.parse(saved);
  } catch(e) {}

  say("Welcome to the commons. Rooms: stage (top-left), breakout tatami (bottom-left), library kiosks (top-right), board & karaoke (bottom-right). Stamp rally is on — visit all four rooms!");

  // ---- zone hints + stamp rally ----
  STAMPS.forEach(function(layer){
    onEnter(layer, function(){
      if (!visited[layer]) {
        visited[layer] = true; persistStamps();
        say("📍 Stamp collected: " + STAMP_NAMES[layer] + " (" + count() + "/" + STAMPS.length + ")");
        if (count() === STAMPS.length) {
          say("🎉 Stamp rally complete! Leave a note on the common-room board so others know you were here.");
        }
      }
    });
  });
  onEnter("zone/silent-reading", function(){ say("🤫 Quiet reading corner — proximity chat is off here."); });
  onEnter("zone/common-board",  function(){ say("This is the community board. Workshops and labs leave their results here."); });

  // ---- virtual smartphone (lite): persistent overlay buttons ----
  addBtn("kc-schedule", "📅", function(){ openTab(LINKS.schedule, "No schedule linked yet — set LINKS.schedule in scripts/commons.js."); });
  addBtn("kc-wiki",     "📖", function(){ openTab(LINKS.wiki,     "No wiki linked yet — the wiki is the persistent source of truth; set LINKS.wiki."); });
  addBtn("kc-discord",  "💬", function(){ openTab(LINKS.discord,  "No Discord linked yet — set LINKS.discord for the async backbone."); });
  addBtn("kc-help",     "🔔", function(){
    if (LINKS.helpHook) {
      fetch(LINKS.helpHook, { method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ content: "🔔 Help requested in the Commons." }) })
        .then(function(){ say("Help requested — a greeter has been pinged."); })
        .catch(function(){ say("Couldn't reach the help channel — ask in chat."); });
    } else { say("Help bell not wired up yet — ask in chat."); }
  });
}).catch(function(e){ console.error("WA init failed", e); });

function addBtn(id, label, cb){
  try { WA.ui.actionBar.addButton({ id:id, label:label, callback:cb }); }
  catch(e) { console.warn("actionBar unavailable", e); }
}
function count(){ return Object.keys(visited).length; }
function persistStamps(){
  try { WA.player.state.saveVariable("kc_stamps", JSON.stringify(visited), { public:false, persist:true, scope:"world" }); }
  catch(e) { try { WA.player.state.kc_stamps = JSON.stringify(visited); } catch(e2){} }
}
