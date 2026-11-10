#!/usr/bin/env python3
"""Generate the Demo Floor room (maps/floor/floor.tmj) — the session-1 demo
floor, online: arcade wing (the kanji games) + museum wall (the industry
specimens) + stamp rally + trophy + cafe.

Standalone on purpose, same contract as gen_lab_maps.py: does NOT touch
tileset.png, genkan.tmj, commons.tmj or maps/lab/* — reuses the shared
placeholder tileset via a relative path. Station zone layers are named
zone_station_<slug>; slugs must match CONFIG.stations in
scripts/floor/floor.js (cross-checked by eye + the validation snippet in
docs/FLOOR-GUIDE.md).
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps", "floor")
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
    def anchor(self, name, x, y, w=3, h=1):
        """Invisible rectangle object used as a WA popup anchor."""
        self.objects.append({"id": self.oid, "name": name, "rotation": 0, "type": "",
            "visible": True, "width": w*TILE, "height": h*TILE, "x": x*TILE, "y": y*TILE})
        self.oid += 1
    def variable(self, name, default="0"):
        """WA world variable declaration (persist across visits where supported)."""
        self.objects.append({"id": self.oid, "name": name, "rotation": 0,
            "type": "variable", "class": "variable", "visible": False,
            "width": TILE, "height": TILE, "x": 0, "y": 0,
            "properties": props({"default": default, "persist": True})})
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

W, H = 30, 18
r = Room(W, H); floor, walls = r.frame()
r.tl("floor", floor)

# ---------------- arcade wing (left wall): the kanji games ----------------
# cabinet = BLUE screen row + PURPLE body row against the wall; zone pad in front
ARCADE = [("dragontale", "DragonTale", 3), ("radfighters", "Radical Fighters", 8), ("majikana", "Maji Kana", 13)]
deco_cab = r.empty()
for slug, name, y in ARCADE:
    r.fill(deco_cab, 1, y, 2, y, BLUE)       # screen
    r.fill(deco_cab, 1, y+1, 2, y+1, PURPLE) # body
r.tl("deco_cabinets", deco_cab)
for slug, name, y in ARCADE:
    r.zone(f"zone_station_{slug}", 3, y, 4, y+1, PURPLE, opacity=0.5)
    r.label(1, y-1.0, 6, f"🕹 {name}")
    r.anchor(f"popup_{slug}", 3, y-1)

# ---------------- museum wall (right wall): the industry specimens ----------------
MUSEUM = [("wanikani", "WaniKani", 3), ("anki", "Anki", 8), ("duolingo", "Duolingo", 13)]
deco_plq = r.empty()
for slug, name, y in MUSEUM:
    r.fill(deco_plq, 27, y, 28, y, PAPER)    # framed exhibit
    r.fill(deco_plq, 27, y+1, 28, y+1, INK)  # pedestal / plaque
r.tl("deco_plaques", deco_plq)
for slug, name, y in MUSEUM:
    r.zone(f"zone_station_{slug}", 25, y, 26, y+1, BLUE, opacity=0.5)
    r.label(24, y-1.0, 5, f"🏛 {name}")
    r.anchor(f"popup_{slug}", 24, y-1)

# ---------------- top nook: poster wall + common board ----------------
r.zone("zone_poster", 11, 1, 12, 2, LANTERN, opacity=0.8)
r.label(10, 3.1, 5, "📜 Poster wall")
r.anchor("popup_poster", 10, 3)
r.zone("zone_board", 17, 1, 18, 2, GREEN, opacity=0.8)
r.label(16, 3.1, 5, "📌 Board")
r.anchor("popup_board", 16, 3)

# ---------------- centre: trophy pedestal (stamp rally goal) ----------------
r.zone("zone_trophy", 13, 7, 16, 10, STAGE_RED, opacity=0.3)
deco_tr = r.empty(); r.fill(deco_tr, 14, 8, 15, 9, GOLD); r.tl("deco_trophy", deco_tr)
r.label(12.5, 6.35, 7, "🏆 スタンプラリー")
r.anchor("popup_trophy", 13, 6, w=4)

# ---------------- cafe corner (voice) ----------------
r.zone("zone_cafe", 24, 15, 28, 16, TATAMI, {"jitsiRoom": "kc-floor-cafe"}, opacity=1.0)
r.label(24.1, 15.08, 6, "🍵 Floor café — voice")

# ---------------- exit to genkan (bottom-left) ----------------
for x in range(2, 4): walls[17*W+x] = 0
z = r.empty(); r.fill(z, 2, 17, 3, 17, TORII)
r.tl("exit-genkan", z, {"exitUrl": "../genkan.tmj"}, 0.7)
r.label(1.2, 16.0, 5, "→ 玄関 Genkan")

# ---------------- signage ----------------
r.label(10.5, 4.4, 9, "ゲームフロア\nDEMO FLOOR — online", 13)
r.label(9.5, 15.2, 12, "Walk onto a glowing pad → popup → stamp.\nAll 6 stamps? Visit the 🏆 in the centre.")

# world variable: completion counter shown at the trophy
r.variable("kc_floor_finishers", "0")

layers = r.dump(f"{OUT}/floor.tmj",
    {"script": "../../scripts/floor/floor.js",
     "mapName": "Demo Floor — online",
     "mapDescription": "The workshop demo floor, online: arcade cabinets for the kanji games, a museum wall for the industry apps, and a stamp rally across all six."},
    walls, (14, 13, 15, 14))
print("floor.tmj layers:", layers)
