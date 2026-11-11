#!/usr/bin/env python3
"""Generate the two themed test rooms (maps/floor/study.tmj + arcade.tmj).

Same demostand roster + quest in both rooms (shared scripts/floor/theme.js);
walking the door between them is the "skin toggle". Art comes from two custom
tilesets packed out of the WA-preset packs (Pipoya base chip + LimeZu room
packs) — see maps/floor/tilesets/COPYRIGHT.md. Objects were extracted as
complete sprites (eye-verified catalog); kc_pack.json maps names -> tile rects.

Standalone on purpose: does NOT touch tileset.png, genkan/commons/lab/floor.
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "maps", "floor")
TS = os.path.join(OUT, "tilesets")
T = 32
PACK = json.load(open(os.path.join(TS, "kc_pack.json"), encoding="utf-8"))
BCOLS, BROWS = PACK["base_size"]
OCOLS, OROWS = PACK["objects_size"]
BASE_FIRST = 1
OBJ_FIRST = BASE_FIRST + BCOLS * BROWS

def bgid(name, i=0):
    c, r, w, h = PACK["base"][name]
    return BASE_FIRST + r * BCOLS + c + min(i, w - 1)

def bvar(name):
    return PACK["base"][name][2]

def odim(name):
    c, r, w, h = PACK["objects"][name]
    return w, h

NONSOLID = {"rug_blue", "rug_pink", "rug_purple", "rug_red", "stage", "spot",
            "banner_purple", "banner_crest", "glass_red", "glass_mosaic",
            "map_frame", "landscape", "portrait", "worldmap", "medal_frames",
            "bell", "lamp_wall", "scroll_map", "books_open", "book_red",
            "teapot", "teacup", "window_curt", "candelabra",
            "door_arch", "door_redgold"}

def props(d):
    out = []
    for k, v in d.items():
        t = "bool" if isinstance(v, bool) else ("int" if isinstance(v, int) else "string")
        out.append({"name": k, "type": t, "value": v})
    return out

class Room:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.ground = [0] * (W * H)
        self.ground2 = [0] * (W * H)
        self.decos = []
        self.col = [0] * (W * H)
        self.zones = []
        self.objects = []; self.oid = 1
        self.lid = 1
    def fill(self, x0, y0, x1, y1, name, i=0):
        g = bgid(name, i)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.ground[y * self.W + x] = g
    def paint(self, x, y, name, i=0, layer=None):
        (layer if layer is not None else self.ground2)[y * self.W + x] = bgid(name, i)
    def paint_rect(self, x0, y0, x1, y1, name, i=0, layer=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.paint(x, y, name, i, layer)
    def block(self, x0, y0, x1=None, y1=None):
        x1 = x0 if x1 is None else x1; y1 = y0 if y1 is None else y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.col[y * self.W + x] = bgid("col")
    def unblock(self, x0, y0, x1=None, y1=None):
        x1 = x0 if x1 is None else x1; y1 = y0 if y1 is None else y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.col[y * self.W + x] = 0
    def hwall(self, x0, x1, y, kit_a, kit_b, gaps=()):
        na, nb = bvar(kit_a), bvar(kit_b)
        for x in range(x0, x1 + 1):
            if any(g0 <= x <= g1 for g0, g1 in gaps): continue
            self.paint(x, y, kit_a, (x - x0) % na)
            self.paint(x, y + 1, kit_b, (x - x0) % nb)
            self.block(x, y, x, y + 1)
    def hband(self, x0, x1, y, kit_a, kit_b, solid=True):
        na, nb = bvar(kit_a), bvar(kit_b)
        for x in range(x0, x1 + 1):
            self.paint(x, y, kit_a, (x - x0) % na)
            self.paint(x, y + 1, kit_b, (x - x0) % nb)
            if solid: self.block(x, y, x, y + 1)
    def vwall(self, x, y0, y1, name, i=0, gaps=()):
        for y in range(y0, y1 + 1):
            if any(g0 <= y <= g1 for g0, g1 in gaps): continue
            self.paint(x, y, name, i)
            self.block(x, y)
    def obj(self, x, y, name, solid=None):
        c, r, w, h = PACK["objects"][name]
        target = None
        for d in self.decos:
            if all(d[(y + dy) * self.W + (x + dx)] == 0
                   for dy in range(h) for dx in range(w)):
                target = d; break
        if target is None:
            target = [0] * (self.W * self.H); self.decos.append(target)
        for dy in range(h):
            for dx in range(w):
                target[(y + dy) * self.W + (x + dx)] = OBJ_FIRST + (r + dy) * OCOLS + (c + dx)
        if solid is None: solid = name not in NONSOLID
        if solid: self.block(x, y, x + w - 1, y + h - 1)
        return w, h
    def zone(self, name, x0, y0, x1, y1, p=None):
        d = [0] * (self.W * self.H)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                d[y * self.W + x] = bgid("zone")
        self.zones.append((name, d, p or {}))
    def anchor(self, name, x, y, w=3, h=1):
        self.objects.append({"id": self.oid, "name": name, "rotation": 0, "type": "",
            "visible": True, "width": w * T, "height": h * T, "x": x * T, "y": y * T})
        self.oid += 1
    def label(self, x, y, text, size=10, color="#2E2A33", w=5):
        self.objects.append({"id": self.oid, "name": "lbl%d" % self.oid, "rotation": 0,
            "text": {"text": text, "wrap": True, "color": color, "fontfamily": "sans-serif", "pixelsize": size},
            "type": "", "visible": True, "width": w * T, "height": T, "x": x * T, "y": y * T})
        self.oid += 1
    def variable(self, name, default="0"):
        self.objects.append({"id": self.oid, "name": name, "rotation": 0,
            "type": "variable", "class": "variable", "visible": False,
            "width": T, "height": T, "x": 0, "y": 0,
            "properties": props({"default": default, "persist": True})})
        self.oid += 1
    def tl(self, name, data, p=None, opacity=1.0):
        l = {"data": data, "height": self.H, "width": self.W, "id": self.lid, "name": name,
             "opacity": opacity, "type": "tilelayer", "visible": True, "x": 0, "y": 0}
        if p: l["properties"] = props(p)
        self.lid += 1
        return l
    def dump(self, path, mapprops, start_rect, exits=()):
        layers = [self.tl("ground", self.ground), self.tl("ground2", self.ground2)]
        for i, d in enumerate(self.decos):
            layers.append(self.tl("deco%d" % i, d))
        for name, d, p in self.zones:
            layers.append(self.tl(name, d, p, opacity=0))
        for name, x0, y0, x1, y1, url in exits:
            d = [0] * (self.W * self.H)
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    d[y * self.W + x] = bgid("zone")
                    self.col[y * self.W + x] = 0
            layers.append(self.tl(name, d, {"exitUrl": url}, opacity=0))
        s = [0] * (self.W * self.H)
        x0, y0, x1, y1 = start_rect
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s[y * self.W + x] = bgid("zone")
        layers.append(self.tl("start", s, opacity=0))
        layers.append(self.tl("collisions", self.col, opacity=0))
        layers.append({"draworder": "topdown", "id": self.lid, "name": "floorLayer",
                       "objects": self.objects, "opacity": 1, "type": "objectgroup",
                       "visible": True, "x": 0, "y": 0}); self.lid += 1
        tilesets = [
            {"columns": BCOLS, "firstgid": BASE_FIRST, "image": "tilesets/kc_base.png",
             "imageheight": BROWS * T, "imagewidth": BCOLS * T, "margin": 0,
             "name": "kc_base", "spacing": 0, "tilecount": BCOLS * BROWS,
             "tileheight": T, "tilewidth": T,
             "tiles": [{"id": bgid("col") - BASE_FIRST,
                        "properties": [{"name": "collides", "type": "bool", "value": True}]}],
             "properties": props({"tilesetCopyright": "Pipoya / LimeZu / WorkAdventure preset tiles, repacked — see tilesets/COPYRIGHT.md"})},
            {"columns": OCOLS, "firstgid": OBJ_FIRST, "image": "tilesets/kc_objects.png",
             "imageheight": OROWS * T, "imagewidth": OCOLS * T, "margin": 0,
             "name": "kc_objects", "spacing": 0, "tilecount": OCOLS * OROWS,
             "tileheight": T, "tilewidth": T,
             "properties": props({"tilesetCopyright": "Pipoya / LimeZu / WorkAdventure preset objects, repacked — see tilesets/COPYRIGHT.md"})}]
        m = {"compressionlevel": -1, "height": self.H, "width": self.W, "infinite": False,
             "layers": layers, "nextlayerid": self.lid, "nextobjectid": self.oid,
             "orientation": "orthogonal", "renderorder": "right-down", "tiledversion": "1.10.2",
             "tileheight": T, "tilewidth": T, "type": "map", "version": "1.10",
             "properties": props(mapprops), "tilesets": tilesets}
        json.dump(m, open(path, "w"), indent=1)
        return [l["name"] for l in layers]

STANDS = [
    ("dragontale",  "DragonTale"), ("radfighters", "Radical Fighters"),
    ("majikana",    "Maji Kana"),  ("kanjicats",   "Kanji Cats"),
    ("nihongosdx",  "Nihongo Showdown DX"), ("Zen Hanzi", "Zen Hanzi"),
    ("kanjistriker","Kanji Striker"), ("wanikani", "WaniKani"),
    ("anki",        "Anki"), ("duolingo", "Duolingo"),
]
NAMES = dict(STANDS)

def booth(r, slug, pad, voice, label_at, label_color="#2E2A33"):
    px, py = pad
    r.paint_rect(px, py, px + 1, py + 1, "path")
    r.zone("voice_" + slug, *voice,
           p={"jitsiRoom": "kc-stand-" + slug, "jitsiTrigger": "onaction",
              "jitsiTriggerMessage": NAMES[slug] + " voice table — watch & discuss"})
    r.zone("zone_stand_" + slug, px, py, px + 1, py + 1)
    r.anchor("popup_" + slug, px - 1, py - 1)
    r.label(label_at[0], label_at[1], NAMES[slug], 10, label_color, 4)

# ============================ STUDY HALL (temple precinct) ============================
def build_study():
    W, H = 44, 30
    r = Room(W, H)
    r.fill(0, 0, W - 1, H - 1, "grass")
    r.block(0, 0, W - 1, 0); r.block(0, H - 1, W - 1, H - 1)
    r.block(0, 0, 0, H - 1); r.block(W - 1, 0, W - 1, H - 1)
    for x in range(0, W - 1, 3):
        r.paint(x, H - 1, "fence", 0)
    # garden greenery
    for (x, y) in [(0, 0), (36, 0), (0, 10), (40, 1), (0, 19), (0, 24), (39, 23), (25, 23), (5, 21), (12, 24)]:
        r.obj(x, y, "tree_green" if (x + y) % 2 == 0 else "tree_autumn")
    for (x, y) in [(6, 18), (28, 19), (37, 20)]:
        r.obj(x, y, "bush_green")
    r.obj(15, 19, "pot_plant"); r.obj(27, 26, "pot_plant"); r.obj(4, 27, "agave")
    # ---- main hall x6..33: roof band rows 2-3, walls 4-5 / 14-15, floor 6-13
    r.paint_rect(7, 6, 32, 13, "wood", layer=r.ground)
    r.hband(6, 33, 2, "roof_a", "roof_b")
    r.hwall(6, 33, 4, "shoji_a", "shoji_b")
    r.hwall(6, 33, 14, "shoji_a", "shoji_b", gaps=((19, 20),))
    r.vwall(6, 4, 15, "beam_b", 1)
    r.vwall(33, 4, 15, "beam_b", 1)
    r.paint_rect(6, 16, 43, 16, "wood", layer=r.ground)      # engawa runs to the annex
    r.paint_rect(19, 15, 20, 17, "path", layer=r.ground)
    r.unblock(19, 14, 20, 15)
    # N-wall dressing
    r.obj(9, 4, "bell"); r.obj(32, 4, "lamp_wall")
    r.obj(16, 4, "glass_red"); r.obj(25, 4, "glass_mosaic")
    # poster wall + board (N wall)
    r.obj(11, 4, "map_frame")
    r.zone("zone_poster", 11, 6, 12, 7)
    r.anchor("popup_poster", 10, 5)
    r.label(10.8, 7.5, "poster wall", 9)
    r.obj(27, 4, "worldmap")
    r.zone("zone_board", 27, 6, 28, 7)
    r.anchor("popup_board", 26, 5)
    r.label(27.1, 7.5, "board 掲示板", 9)
    # trophy shrine centre-N
    r.obj(18, 6, "rug_red")
    r.obj(17, 6, "column_tan"); r.obj(22, 6, "column_tan")
    r.obj(19, 5, "shrine_shelf")
    r.obj(20, 6, "trophy_g1"); r.obj(21, 6, "trophy_g2")
    r.obj(19, 8, "chest_gold"); r.obj(22, 8, "chest_red")
    r.zone("zone_trophy", 18, 7, 21, 9)
    r.anchor("popup_trophy", 18, 6, w=4)
    r.label(17.8, 3.15, "スタンプラリー", 11, "#F2E8D5", 5)
    # N-wall stands: WaniKani + Anki (glass counters)
    r.obj(13, 6, "glasscounter")
    booth(r, "wanikani", pad=(14, 8), voice=(12, 6, 16, 9), label_at=(13.6, 9.6))
    r.obj(23, 6, "glasscounter")
    booth(r, "anki", pad=(24, 8), voice=(22, 6, 26, 9), label_at=(24.1, 9.6))
    # W wall: own games (retro pc desks)
    for slug, y in [("dragontale", 6), ("radfighters", 9), ("majikana", 12)]:
        r.obj(7, y, "pcdesk")
        if y < 12: r.obj(7, y + 2, "bonsai")
        booth(r, slug, pad=(9, y), voice=(7, y - 1, 11, y + 2), label_at=(8.7, y + 2.1))
    # E wall: public demos (display cabinets)
    for slug, y in [("kanjicats", 6), ("nihongosdx", 9), ("Zen Hanzi", 12)]:
        r.obj(31, y - 1, "dispcab_a")
        booth(r, slug, pad=(29, y), voice=(28, y - 1, 32, y + 1), label_at=(28.4, y + 2.1))
    # Kanji Striker nook (centre-south)
    r.obj(13, 11, "desk_mon")
    booth(r, "kanjistriker", pad=(16, 11), voice=(13, 10, 18, 13), label_at=(14.8, 13.2))
    # ---- annex x34..43: roof rows 4-5? (lower building) walls 6-7 / 14-15
    r.paint_rect(35, 8, 42, 13, "tatami", layer=r.ground)
    r.hband(34, 43, 4, "roof_a", "roof_b")
    r.hwall(34, 43, 6, "beam_a", "beam_b")
    r.hwall(34, 43, 14, "beam_a", "beam_b", gaps=((38, 39),))
    r.vwall(34, 6, 15, "beam_b", 1)
    r.vwall(43, 6, 15, "beam_b", 1)
    r.paint_rect(38, 14, 39, 15, "tatami", layer=r.ground)
    # library + piano + clock (keep the entry corridor x35-36 rows 9-10 clear)
    r.obj(37, 8, "bookshelf_s"); r.obj(38, 8, "piano")
    r.obj(40, 8, "shelf_half"); r.obj(42, 11, "gclock")
    # cafe (annex south; keep the door corridor x38-39 clear)
    r.obj(35, 12, "donutcase")
    r.obj(40, 12, "table_wood")
    r.obj(40, 12, "teapot", solid=False); r.obj(41, 12, "teacup", solid=False)
    r.obj(35, 11, "stool_y"); r.obj(41, 13, "stool_r")
    r.zone("zone_cafe", 35, 11, 41, 13, {"jitsiRoom": "kc-floor-cafe"})
    r.label(36.3, 13.45, "cafe 茶屋", 9)
    # duolingo garden nook (SE)
    r.obj(29, 19, "bench_or")
    booth(r, "duolingo", pad=(30, 20), voice=(28, 18, 33, 22), label_at=(29.6, 21.6))
    # garden focal: fountain + path + gate + statues
    r.obj(18, 20, "fountain")
    r.paint_rect(19, 17, 20, 19, "path", layer=r.ground)
    r.paint_rect(19, 23, 20, 28, "path", layer=r.ground)
    r.obj(17, 24, "statue"); r.obj(22, 24, "statue")
    r.obj(19, 26, "door_redgold")
    r.label(21.2, 26.3, "⛩ → 玄関", 10, "#F2E8D5", 4)
    # east gate to arcade
    r.obj(41, 17, "door_arch")
    r.paint_rect(42, 17, 43, 18, "path", layer=r.ground)
    r.unblock(43, 17, 43, 18)
    r.label(39.0, 19.3, "→ arcade", 10, "#F2E8D5", 4)
    r.variable("kc_floor_finishers", "0")
    layers = r.dump(os.path.join(OUT, "study.tmj"),
        {"script": "../../scripts/floor/theme.js",
         "mapName": "Kanji Study Hall 書斎",
         "mapDescription": "Temple-precinct study hall: demostand booths, stamp rally, library annex and garden. The east gate leads to the arcade skin of the same floor."},
        (19, 24, 20, 25),
        exits=[("exit-genkan", 19, 29, 20, 29, "../genkan.tmj"),
               ("exit-arcade", 43, 17, 43, 18, "arcade.tmj")])
    print("study.tmj", len(layers), "layers")

# ============================ ARCADE CELLAR ============================
def build_arcade():
    W, H = 40, 24
    r = Room(W, H)
    r.fill(0, 0, W - 1, H - 1, "wood_dk")
    r.hwall(0, W - 1, 0, "brick_a", "brick_b", gaps=((2, 3), (5, 6)))
    for x in range(24, 36):
        r.paint(x, 0, "arch_a", (x - 24) % 6); r.paint(x, 1, "arch_b", (x - 24) % 6)
        r.block(x, 0, x, 1)
    r.paint_rect(1, H - 1, W - 2, H - 1, "brick_b", 1)
    r.block(0, H - 1, W - 1, H - 1)
    r.vwall(0, 1, H - 2, "brick_b", 1); r.vwall(W - 1, 1, H - 2, "brick_b", 1)
    # exits through the north wall (door art sits in the gaps)
    r.obj(2, 0, "door_arch"); r.obj(5, 0, "door_arch")
    r.label(1.4, 2.2, "→ 玄関", 9, "#F2E8D5", 3)
    r.label(4.5, 2.2, "↑ study hall", 9, "#F2E8D5", 4)
    # partitions: lounge | stage room, lounge | alley
    r.vwall(22, 2, 11, "brick_b", 1, gaps=((6, 7),))
    r.hwall(1, W - 2, 11, "brick_a", "brick_b", gaps=((6, 7), (26, 27)))
    # ---- bar lounge
    r.obj(3, 3, "counter_big")
    r.obj(11, 2, "vending")
    r.obj(13, 2, "claw_a"); r.obj(15, 2, "claw_b")
    r.obj(18, 0, "map_frame")
    r.zone("zone_poster", 18, 2, 19, 3)
    r.anchor("popup_poster", 17, 1)
    r.label(17.7, 3.6, "poster wall", 9, "#F2E8D5")
    r.obj(20, 0, "worldmap")
    r.zone("zone_board", 20, 2, 21, 3)
    r.anchor("popup_board", 19, 1)
    r.label(19.9, 3.6, "board", 9, "#F2E8D5")
    r.obj(2, 7, "booth_sofa")
    r.obj(6, 7, "sofa_grey")
    r.obj(10, 8, "table_wood"); r.obj(9, 8, "stool_r"); r.obj(12, 8, "stool_b")
    r.zone("zone_cafe", 4, 6, 10, 7, {"jitsiRoom": "kc-floor-cafe"})
    r.label(4.1, 5.6, "bar — voice", 9, "#F2E8D5")
    # ---- stage room
    r.obj(26, 2, "spot"); r.obj(28, 2, "spot"); r.obj(30, 2, "spot")
    r.obj(26, 3, "stage")
    r.obj(27, 3, "podium", solid=False)
    r.obj(24, 4, "speaker"); r.obj(31, 4, "speaker")
    r.obj(26, 7, "stool_y"); r.obj(28, 7, "stool_r"); r.obj(30, 7, "stool_b")
    r.label(26.4, 6.4, "DEMO STAGE", 10, "#F2E8D5", 4)
    r.obj(33, 0, "medal_frames")
    r.obj(34, 3, "rug_blue")
    r.obj(35, 3, "trophy_g1"); r.obj(36, 3, "trophy_g2"); r.obj(37, 3, "cup_silver")
    r.obj(34, 5, "chest_gold"); r.obj(37, 5, "chest_red")
    r.zone("zone_trophy", 34, 4, 37, 6)
    r.anchor("popup_trophy", 34, 3, w=4)
    r.label(33.7, 6.9, "スタンプラリー", 10, "#F2E8D5", 5)
    r.obj(23, 8, "pool_green")
    r.obj(36, 8, "servers")
    # ---- alley: 7 game cabinets N side, industry desks S side
    cabs = ["arcade1", "arcade2", "arcade3"]
    banners = ["banner_crest", "banner_purple"]
    for i, (x, slug) in enumerate([(2, "dragontale"), (7, "radfighters"), (12, "majikana"),
                                   (17, "kanjicats"), (22, "nihongosdx"), (27, "Zen Hanzi"), (32, "kanjistriker")]):
        r.obj(x, 13, cabs[i % 3])
        r.obj(x + 2, 11, banners[i % 2], solid=False)
        booth(r, slug, pad=(x, 16), voice=(x - 1, 13, x + 2, 18),
              label_at=(x - 0.4, 17.7), label_color="#F2E8D5")
    for x, slug in [(5, "wanikani"), (16, "anki"), (27, "duolingo")]:
        r.obj(x, 20, "desk_mon")
        booth(r, slug, pad=(x + 3, 20), voice=(x, 19, x + 4, 22),
              label_at=(x + 2.6, 18.7), label_color="#F2E8D5")
    # roped-off future corner
    r.obj(36, 19, "crate"); r.obj(37, 21, "pot_big")
    for x in (35, 36, 37, 38):
        r.paint(x, 18, "fence", (x - 35) % 3); r.block(x, 18)
    r.label(34.9, 18.7, "coming soon", 9, "#D9A84E", 4)
    r.variable("kc_floor_finishers", "0")
    layers = r.dump(os.path.join(OUT, "arcade.tmj"),
        {"script": "../../scripts/floor/theme.js",
         "mapName": "Kanji Game Lounge",
         "mapDescription": "Arcade-cellar skin of the floor: the same demostand booths and stamp rally as the study hall, plus a demo stage. The stairs lead back up."},
        (12, 8, 13, 9),
        exits=[("exit-genkan", 2, 1, 3, 1, "../genkan.tmj"),
               ("exit-study", 5, 1, 6, 1, "study.tmj")])
    print("arcade.tmj", len(layers), "layers")

if __name__ == "__main__":
    build_study()
    build_arcade()
