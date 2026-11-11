#!/usr/bin/env python3
"""Generate the Feature Lab maps (maps/lab/*.tmj) — one room per feature cluster.

Standalone on purpose: does NOT touch tileset.png, genkan.tmj or commons.tmj
(those stay owned by gen_maps.py). Reuses the same placeholder tileset via a
relative path. Zone layer names follow the Gemini catalog convention
`zone_topicN_<feature>` so docs/gemini-artifacts/TOPIC-MATRIX.md stays the
cross-reference. Each room is exit-linked to hub.tmj; the hub links onward to
../genkan.tmj (the existing world is never modified).
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps", "lab")
os.makedirs(OUT, exist_ok=True)
TILE = 32; COLS_TS = 4; ROWS_TS = 4

# gids from the shared placeholder tileset (see gen_maps.py palette)
FLOOR_L, FLOOR_D, WALL, TATAMI, WOOD, STAGE_RED, PAPER, BLUE, PURPLE, GREY, GREEN, GOLD, CORRIDOR, TORII, INK, LANTERN = range(1, 17)

def tileset():
    return [{"columns": COLS_TS, "firstgid": 1, "image": "../tileset.png",
             "imageheight": ROWS_TS*TILE, "imagewidth": COLS_TS*TILE, "margin": 0,
             "name": "kanji-commons-placeholder", "spacing": 0,
             "tilecount": COLS_TS*ROWS_TS, "tileheight": TILE, "tilewidth": TILE,
             "tiles": [{"id": 2, "properties": [{"name": "collides", "type": "bool", "value": True}]}]}]

def props(d_):
    return [{"name": k, "type": ("bool" if isinstance(v, bool) else "string"), "value": v} for k, v in d_.items()]

class Room:
    def __init__(self, W, H):
        self.W, self.H = W, H; self.layers = []; self.lid = 1
        self.objects = []; self.oid = 1
    def empty(self): return [0]*(self.W*self.H)
    def fill(self, layer, x0, y0, x1, y1, gid):
        for y in range(y0, y1+1):
            for x in range(x0, x1+1): layer[y*self.W+x] = gid
    def tl(self, name, data, p=None, opacity=1.0):
        l = {"data": data, "height": self.H, "width": self.W, "id": self.lid, "name": name,
             "opacity": opacity, "type": "tilelayer", "visible": True, "x": 0, "y": 0}
        if p: l["properties"] = props(p)
        self.lid += 1; self.layers.append(l)
    def label(self, x, y, w, text, size=9, color="#2E2A33"):
        self.objects.append({"id": self.oid, "name": f"lbl{self.oid}", "rotation": 0,
            "text": {"text": text, "wrap": True, "color": color, "fontfamily": "sans-serif", "pixelsize": size},
            "type": "", "visible": True, "width": w*TILE, "height": TILE, "x": x*TILE, "y": y*TILE})
        self.oid += 1
    def zone(self, name, x0, y0, x1, y1, gid, p=None, opacity=0.45, lbl=None):
        l = self.empty(); self.fill(l, x0, y0, x1, y1, gid)
        self.tl(name, l, p, opacity)
        if lbl: self.label(x0, max(0, y0-1)+0.0, (x1-x0+1)+2, lbl)
    def frame(self):
        floor = self.empty()
        for y in range(self.H):
            for x in range(self.W): floor[y*self.W+x] = FLOOR_L if (x+y) % 2 == 0 else FLOOR_D
        walls = self.empty()
        self.fill(walls, 0, 0, self.W-1, 0, WALL); self.fill(walls, 0, self.H-1, self.W-1, self.H-1, WALL)
        for y in range(self.H): walls[y*self.W+0] = WALL; walls[y*self.W+self.W-1] = WALL
        return floor, walls
    def dump(self, path, mapprops, walls, start_rect):
        s = self.empty(); self.fill(s, *start_rect, GOLD)
        self.tl("walls", walls)
        self.layers.append({"draworder": "topdown", "id": self.lid, "name": "floorLayer",
                            "objects": self.objects, "opacity": 1, "type": "objectgroup",
                            "visible": True, "x": 0, "y": 0}); self.lid += 1
        self.tl("start", s, opacity=0.6)
        m = {"compressionlevel": -1, "height": self.H, "width": self.W, "infinite": False,
             "layers": self.layers, "nextlayerid": self.lid, "nextobjectid": self.oid,
             "orientation": "orthogonal", "renderorder": "right-down", "tiledversion": "1.10.2",
             "tileheight": TILE, "tilewidth": TILE, "type": "map", "version": "1.10",
             "properties": props(mapprops), "tilesets": tileset()}
        json.dump(m, open(path, "w"), indent=1)
        for l in m["layers"]:
            if l["type"] == "tilelayer": assert len(l["data"]) == self.W*self.H, (path, l["name"])
        return [l["name"] for l in m["layers"]]

def mp(name, desc, script):
    return {"script": f"../../scripts/lab/{script}", "mapName": f"KC Lab — {name}", "mapDescription": desc}

W, H = 24, 14

# ---------------- HUB ----------------
r = Room(24, 16); floor, walls = r.frame()
r.tl("floor", floor)
doors = [  # (layer, target, x0,y0,x1,y1, label x offset)
    ("exit-onboarding", "./onboarding.tmj", 4, 0, 5, 0),
    ("exit-social", "./social.tmj", 11, 0, 12, 0),
    ("exit-pedagogy", "./pedagogy.tmj", 18, 0, 19, 0),
    ("exit-data", "./data.tmj", 23, 5, 23, 6),
    ("exit-collab", "./collab.tmj", 23, 10, 23, 11),
    ("exit-persistence", "./persistence.tmj", 11, 15, 12, 15),
    ("exit-integrations", "./integrations.tmj", 0, 5, 0, 6),
    ("exit-genkan", "../genkan.tmj", 4, 15, 5, 15),
]
for name, url, x0, y0, x1, y1 in doors:
    for x in range(x0, x1+1):
        for y in range(y0, y1+1): walls[y*24+x] = 0   # cut door out of wall
    z = r.empty(); r.fill(z, x0, y0, x1, y1, TORII)
    r.tl(name, z, {"exitUrl": url}, 0.7)
labels = [(3, 1, "① Onboarding\ntopics 1–3"), (10, 1, "② Social\n4·5·12"), (17, 1, "③ Pedagogy\n6·10·19"),
          (19.5, 4.6, "④ Data\n8·9·11"), (19.5, 9.6, "⑤ Collab\n7·13·15"), (10, 13.4, "⑥ Persistence\n17·18·20"),
          (1.2, 4.6, "⑦ Integrations\n14·16·hooks"), (2.8, 13.4, "→ Genkan\n(main world)")]
for x, y, t in labels: r.label(x, y, 5, t)
r.label(7, 7, 10, "漢字コモンズ FEATURE LAB\nEach door = one testable feature cluster.\nSee docs/LAB-REVIEW-GUIDE.md", 11)
r.zone("zone_welcome", 9, 6, 14, 9, PAPER, opacity=0.3)
r.dump(f"{OUT}/hub.tmj", mp("Hub", "Feature-lab hub: doors to 7 modular test rooms. Placeholder art by design.", "hub.js"),
       walls, (11, 11, 12, 12))

# ---------------- ① ONBOARDING (topics 1,2,3) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic1_airlock", 1, 10, 5, 12, GREY, lbl="T1 Airlock — click to unlock")
b = r.empty(); r.fill(b, 6, 10, 6, 12, WALL)
r.tl("barrier_topic1_airlock", b, opacity=0.9)          # hidden by script => collision gone
for i, x in enumerate(range(7, 15)):                     # T1 option C: ghost-guide floor path
    g = None
    if i % 2 == 0:
        gl = r.empty(); r.fill(gl, x, 11, x, 11, LANTERN); r.tl(f"deco_ghostpath_{i}", gl, opacity=0.5)
r.zone("zone_topic2_audiocircle", 16, 9, 21, 12, GREEN, {"jitsiRoom": "kc-lab-audiocircle"},
       lbl="T2 Audio circle (proximity voice)")
r.zone("zone_topic3_flag_en", 3, 3, 5, 5, BLUE, lbl="T3 English")
r.zone("zone_topic3_flag_jp", 8, 3, 10, 5, STAGE_RED, lbl="T3 日本語")
r.zone("exit-hub", 22, 6, 23, 7, TORII, {"exitUrl": "./hub.tmj"}, 0.7, lbl="→ Hub")
walls[6*24+23] = 0; walls[7*24+23] = 0
r.dump(f"{OUT}/onboarding.tmj", mp("Onboarding", "Topics 1-3: airlock spawn w/ unlockable barrier, ghost path, proximity ring, language tiles.", "onboarding.js"),
       walls, (2, 11, 3, 12))

# ---------------- ② SOCIAL (topics 4,5,12) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic4_speeddate", 2, 9, 7, 12, PURPLE, {"jitsiRoom": "kc-lab-speeddate"},
       lbl="T4 Speed-dating ring (timed)")
r.zone("zone_topic5_stage", 9, 2, 15, 5, STAGE_RED, {"jitsiRoom": "kc-lab-stage"},
       lbl="T5 Stage (megaphone = plan-gated)")
r.zone("zone_topic12_role_developer", 17, 9, 18, 10, BLUE, lbl="T12 DEV")
r.zone("zone_topic12_role_educator", 20, 9, 21, 10, GREEN, lbl="T12 EDU")
r.zone("zone_topic12_role_researcher", 17, 12, 18, 12, GOLD, lbl="T12 RES")
r.zone("exit-hub", 11, 13, 12, 13, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[13*24+11] = 0; walls[13*24+12] = 0
r.dump(f"{OUT}/social.tmj", mp("Social", "Topics 4,5,12: speed-dating timer bubble, stage w/ camera cue, role-tag zones with outlines.", "social.js"),
       walls, (11, 11, 12, 12))

# ---------------- ③ PEDAGOGY (topics 6,10,19) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic6_cogload", 2, 2, 5, 4, PAPER, lbl="T6 Cognitive-load testbench")
r.zone("zone_topic6_radical_lab", 8, 2, 11, 4, WOOD, lbl="T6 Radical decomposition lab")
for i in range(5):                                       # T10: Leitner boxes as walkable strip
    x0 = 2 + i*4
    r.zone(f"zone_topic10_leitner_box{i+1}", x0, 8, x0+2, 10, [GREY, BLUE, GREEN, GOLD, STAGE_RED][i],
           lbl=f"T10 Box {i+1}")
r.zone("zone_topic19_eval_matrix", 14, 2, 18, 4, GREEN, lbl="T19 Pedagogy eval matrix")
r.zone("exit-hub", 11, 13, 12, 13, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[13*24+11] = 0; walls[13*24+12] = 0
r.dump(f"{OUT}/pedagogy.tmj", mp("Pedagogy", "Topics 6,10,19: cog-load checklist, radical lab, walkable Leitner SRS boxes (state persists), eval matrix.", "pedagogy.js"),
       walls, (21, 12, 22, 12))

# ---------------- ④ DATA (topics 8,9,11) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic8_api", 2, 2, 5, 4, BLUE, lbl="T8 kanjiapi.dev live kiosk")
r.zone("zone_topic9_tracing", 8, 2, 11, 4, PAPER, lbl="T9 KanjiVG (script embed)")
r.zone("zone_topic9_tracing_prop", 14, 2, 17, 4, PAPER,
       {"openWebsite": "../../web/tracing.html", "openWebsiteTrigger": "onaction",
        "openWebsiteTriggerMessage": "SPACE: tracing kiosk (map-property variant)", "openWebsiteWidth": "55"},
       lbl="T9 KanjiVG (map-prop variant)")
r.zone("zone_topic11_kanjigarden", 2, 8, 5, 11, GREEN, lbl="T11 kanji.garden embed")
r.zone("zone_topic11_influent", 8, 8, 11, 11, PURPLE, lbl="T11 Influent (non-embeddable)")
r.zone("zone_topic11_graveyard", 14, 8, 17, 11, INK, lbl="T11 Academic graveyard (TUM…)")
r.zone("exit-hub", 0, 6, 0, 7, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[6*24+0] = 0; walls[7*24+0] = 0
r.dump(f"{OUT}/data.tmj", mp("Data kiosks", "Topics 8,9,11: live kanjiapi.dev fetch, KanjiVG embeds (script vs map-property), genre museum trio.", "data.js"),
       walls, (21, 12, 22, 12))

# ---------------- ⑤ COLLAB (topics 7,13,15) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic7_etherpad", 2, 2, 5, 4, PAPER, lbl="T7 Etherpad sidebar")
r.zone("zone_topic7_github_terminal", 8, 2, 11, 4, INK, lbl="T7 GitHub commits terminal")
r.zone("zone_topic13_standup", 14, 2, 18, 4, TATAMI, {"jitsiRoom": "kc-lab-standup"}, lbl="T13 Standup circle + pad")
r.zone("zone_topic13_sprint_bell", 2, 8, 4, 10, GOLD, lbl="T13 Sprint bell (Events API)")
r.zone("zone_topic15_excalidraw", 8, 8, 12, 11, GREEN, lbl="T15 Excalidraw table")
r.zone("exit-hub", 0, 6, 0, 7, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[6*24+0] = 0; walls[7*24+0] = 0
r.dump(f"{OUT}/collab.tmj", mp("Collaboration", "Topics 7,13,15: Etherpad, live GitHub terminal, standup circle, Events-API sprint bell, Excalidraw.", "collab.js"),
       walls, (21, 12, 22, 12))

# ---------------- ⑥ PERSISTENCE (topics 17,18,20) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic17_vote_green", 2, 2, 4, 4, GREEN, lbl="T17 Vote: works!")
r.zone("zone_topic17_vote_red", 7, 2, 9, 4, STAGE_RED, lbl="T17 Vote: confusing")
r.zone("zone_topic17_vote_reset", 12, 2, 13, 3, GREY, lbl="T17 Reset tallies")
r.zone("zone_topic18_message_pillar", 16, 2, 18, 4, WOOD, lbl="T18 Message pillar (persists)")
r.zone("zone_topic20_trophy", 2, 8, 5, 11, GOLD, lbl="T20 Trophy room")
r.zone("zone_board_ema", 8, 8, 11, 11, GREEN,
       {"openWebsite": "../../web/board.html", "openWebsiteTrigger": "onaction",
        "openWebsiteTriggerMessage": "SPACE: common board & ema wall", "openWebsiteWidth": "55"},
       lbl="Board / ema wall (existing kiosk)")
r.zone("exit-hub", 11, 0, 12, 0, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[0*24+11] = 0; walls[0*24+12] = 0
r.dump(f"{OUT}/persistence.tmj", mp("Persistence", "Topics 17,18,20: shared-state vote tiles + reset, message pillar, trophy room, ema-board tie-in.", "persistence.js"),
       walls, (11, 11, 12, 12))

# ---------------- ⑦ INTEGRATIONS (topics 14,16 + webhook bench) ----------------
r = Room(W, H); floor, walls = r.frame(); r.tl("floor", floor)
r.zone("zone_topic16_help_button", 2, 2, 4, 4, STAGE_RED, lbl="T16 Help Bell → Discord webhook")
r.zone("zone_topic16_discord_feed", 7, 2, 10, 4, PURPLE, lbl="T16 Discord feed (WidgetBot)")
r.zone("zone_webhook_results", 13, 2, 16, 4, BLUE, lbl="Post event results → Discord")
r.zone("zone_topic14_asset_chest", 2, 8, 4, 10, GOLD, lbl="T14 Data-pack chest")
r.zone("zone_topic14_submission_desk", 7, 8, 10, 10, PAPER, lbl="T14 License checkpoint")
r.zone("zone_calendar", 13, 8, 16, 10, GREEN, lbl="Community calendar embed")
r.zone("exit-hub", 23, 6, 23, 7, TORII, {"exitUrl": "./hub.tmj"}, 0.7)
walls[6*24+23] = 0; walls[7*24+23] = 0
r.dump(f"{OUT}/integrations.tmj", mp("Integrations", "Topics 14,16 + webhook bench: Help Bell, WidgetBot feed, results-poster, asset chest, license desk, calendar.", "integrations.js"),
       walls, (20, 12, 21, 12))

print("OK — lab maps written to", OUT)
