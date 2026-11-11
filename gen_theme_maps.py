#!/usr/bin/env python3
"""Generate the minimal demo showfloor: maps/floor/study.tmj + arcade.tmj.

Two EMPTY rooms (good base textures only, no decor), six demo booths each —
the publicly available session-1 demos + WaniKani + Anki — hooked to
scripts/floor/showfloor.js. Identical geometry in both rooms; the side doors
toggle between the skins. Rooms are deliberately bare so they can be extended
in Tiled / the map editor later.

Tilesets: kc_base.png (repacked WA-preset wall/floor tiles, see COPYRIGHT.md)
+ kc_commons.png (ORIGINAL Kanji Commons pack: booths, pads, dark walls, mats).
Standalone: does NOT touch tileset.png, genkan/commons/lab/floor maps.
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "maps", "floor")
TS = os.path.join(OUT, "tilesets")
T = 32
PACK = json.load(open(os.path.join(TS, "kc_pack.json"), encoding="utf-8"))
BCOLS, BROWS = PACK["base_size"]
BASE_FIRST = 1
KC_FIRST = BASE_FIRST + BCOLS * BROWS
KC_COLS, KC_ROWS = 8, 4

def bgid(name, i=0):
    c, r, w, h = PACK["base"][name]
    return BASE_FIRST + r * BCOLS + c + min(i, w - 1)

def bvar(name):
    return PACK["base"][name][2]

# kc_commons.png slots (col, row, w, h)
KC = {
    "booth_study":  (0, 0, 2, 2), "booth_arcade": (2, 0, 2, 2),
    "pad_study":    (4, 0, 1, 1),
    "pad_cyan":     (5, 0, 1, 1), "pad_mag": (6, 0, 1, 1), "pad_gold": (7, 0, 1, 1),
    "wall_dark":    (4, 1, 1, 1),
    "wall_cyan":    (5, 1, 1, 1), "wall_mag": (6, 1, 1, 1), "wall_gold": (7, 1, 1, 1),
    "mat_study":    (0, 2, 1, 1), "mat_arcade": (1, 2, 1, 1),
    "floor_dark":   (2, 2, 1, 1),
}
def kgid(name, dx=0, dy=0):
    c, r, w, h = KC[name]
    return KC_FIRST + (r + dy) * KC_COLS + (c + dx)

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
        self.walls = [0] * (W * H)
        self.booths = [0] * (W * H)
        self.col = [0] * (W * H)
        self.zones = []
        self.objects = []; self.oid = 1; self.lid = 1
    def g(self, x, y, gid, layer=None):
        (layer if layer is not None else self.ground)[y * self.W + x] = gid
    def fill(self, x0, y0, x1, y1, gid, layer=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.g(x, y, gid, layer)
    def block(self, x0, y0, x1=None, y1=None):
        x1 = x0 if x1 is None else x1; y1 = y0 if y1 is None else y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.col[y * self.W + x] = bgid("col")
    def stamp_kc(self, x, y, name, solid=True):
        c, r, w, h = KC[name]
        for dy in range(h):
            for dx in range(w):
                self.booths[(y + dy) * self.W + (x + dx)] = kgid(name, dx, dy)
        if solid: self.block(x, y, x + w - 1, y + h - 1)
    def zone(self, name, x0, y0, x1, y1, p=None):
        d = [0] * (self.W * self.H)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                d[y * self.W + x] = bgid("zone")
        self.zones.append((name, d, p or {}))
    def anchor(self, name, x, y, w=4, h=1):
        self.objects.append({"id": self.oid, "name": name, "rotation": 0, "type": "",
            "visible": True, "width": w * T, "height": h * T, "x": x * T, "y": y * T})
        self.oid += 1
    def label(self, x, y, text, size=10, color="#2E2A33", w=5):
        self.objects.append({"id": self.oid, "name": "lbl%d" % self.oid, "rotation": 0,
            "text": {"text": text, "wrap": True, "color": color, "fontfamily": "sans-serif",
                     "pixelsize": size, "halign": "center"},
            "type": "", "visible": True, "width": w * T, "height": T, "x": x * T, "y": y * T})
        self.oid += 1
    def tl(self, name, data, p=None, opacity=1.0):
        l = {"data": data, "height": self.H, "width": self.W, "id": self.lid, "name": name,
             "opacity": opacity, "type": "tilelayer", "visible": True, "x": 0, "y": 0}
        if p: l["properties"] = props(p)
        self.lid += 1
        return l
    def dump(self, path, mapprops, start_rect, exits):
        layers = [self.tl("ground", self.ground), self.tl("walls", self.walls),
                  self.tl("booths", self.booths)]
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
             "properties": props({"tilesetCopyright": "WA-preset tiles repacked — see tilesets/COPYRIGHT.md"})},
            {"columns": KC_COLS, "firstgid": KC_FIRST, "image": "tilesets/kc_commons.png",
             "imageheight": KC_ROWS * T, "imagewidth": KC_COLS * T, "margin": 0,
             "name": "kc_commons", "spacing": 0, "tilecount": KC_COLS * KC_ROWS,
             "tileheight": T, "tilewidth": T,
             "properties": props({"tilesetCopyright": "kc_commons: original Kanji Commons pack (this repo), CC0"})}]
        m = {"compressionlevel": -1, "height": self.H, "width": self.W, "infinite": False,
             "layers": layers, "nextlayerid": self.lid, "nextobjectid": self.oid,
             "orientation": "orthogonal", "renderorder": "right-down", "tiledversion": "1.10.2",
             "tileheight": T, "tilewidth": T, "type": "map", "version": "1.10",
             "properties": props(mapprops), "tilesets": tilesets}
        json.dump(m, open(path, "w"), indent=1)
        return [l["name"] for l in layers]

# the showfloor roster: only the publicly available session-1 demos (+ WK, Anki)
BOOTHS = [  # (slug, label, side L|R, slot 0..2)
    ("kanjicats",    "Kanji Cats",          "L", 0),
    ("nihongosdx",   "Nihongo Showdown DX", "L", 1),
    ("bbv01",        "bbv01",               "L", 2),
    ("kanjistriker", "Kanji Striker",       "R", 0),
    ("wanikani",     "WaniKani",            "R", 1),
    ("anki",         "Anki",                "R", 2),
]
W, H = 26, 16
SLOT_Y = [3, 7, 11]

def build(theme):
    r = Room(W, H)
    dark = theme == "arcade"
    ink = "#F2E8D5" if dark else "#2E2A33"
    # floor
    r.fill(0, 0, W - 1, H - 1, kgid("floor_dark") if dark else bgid("wood"))
    # walls: top 2 rows, bottom row, side columns
    if dark:
        trims = ["wall_cyan", "wall_mag", "wall_gold"]
        for x in range(W):
            r.g(x, 0, kgid(trims[(x // 4) % 3]), r.walls)
            r.g(x, 1, kgid("wall_dark"), r.walls)
        for x in range(W):
            r.g(x, H - 1, kgid("wall_dark"), r.walls)
        for y in range(1, H - 1):
            r.g(0, y, kgid("wall_dark"), r.walls)
            r.g(W - 1, y, kgid("wall_dark"), r.walls)
    else:
        na, nb = bvar("shoji_a"), bvar("shoji_b")
        for x in range(W):
            r.g(x, 0, bgid("shoji_a", x % na), r.walls)
            r.g(x, 1, bgid("shoji_b", x % nb), r.walls)
        for x in range(W):
            r.g(x, H - 1, bgid("beam_b", 1), r.walls)
        for y in range(1, H - 1):
            r.g(0, y, bgid("beam_b", 1), r.walls)
            r.g(W - 1, y, bgid("beam_b", 1), r.walls)
    r.block(0, 0, W - 1, 1); r.block(0, H - 1, W - 1, H - 1)
    r.block(0, 0, 0, H - 1); r.block(W - 1, 0, W - 1, H - 1)
    # door gaps between booth rows (study: east -> arcade; arcade: west -> study)
    door_x = W - 1 if theme == "study" else 0
    for y in (9, 10):
        r.g(door_x, y, 0, r.walls)
    mat = "mat_arcade" if dark else "mat_study"
    mx = W - 2 if theme == "study" else 1
    r.stamp_kc(mx, 9, mat, solid=False)
    r.stamp_kc(mx, 10, mat, solid=False)
    r.label(mx - 2.6 if theme == "study" else mx + 0.6, 10.62,
            "→ arcade" if theme == "study" else "→ study hall", 9, ink, 3)
    # booths
    booth_tile = "booth_arcade" if dark else "booth_study"
    pads = ["pad_cyan", "pad_mag", "pad_gold"] if dark else ["pad_study"] * 3
    for slug, name, side, slot in BOOTHS:
        y = SLOT_Y[slot]
        if side == "L":
            bx, px_, lx = 1, 3, 1.5
        else:
            bx, px_, lx = 23, 21, 21.5
        r.stamp_kc(bx, y, booth_tile)
        pad = pads[slot]
        for (zx, zy) in ((px_, y), (px_ + 1, y), (px_, y + 1), (px_ + 1, y + 1)):
            r.g(zx, zy, kgid(pad), r.booths)
        r.zone("zone_stand_" + slug, px_, y, px_ + 1, y + 1)
        r.anchor("popup_" + slug, bx - 1 if side == "L" else bx - 2, y - 1)
        r.label(lx, y + 2.15, name, 10, ink, 4)
    # title
    r.label(10.5, 14.2, "Kanji Commons — demo floor", 10, ink, 5)
    exits = [("exit-arcade", W - 1, 9, W - 1, 10, "arcade.tmj")] if theme == "study" \
        else [("exit-study", 0, 9, 0, 10, "study.tmj")]
    name = "Kanji Study Hall 書斎" if theme == "study" else "Kanji Game Lounge"
    layers = r.dump(os.path.join(OUT, theme + ".tmj"),
        {"script": "../../scripts/floor/showfloor.js",
         "mapName": name,
         "mapDescription": "Kanji Commons demo showfloor — walk to a booth and press the button to open its demo. The side door switches the room style."},
        (12, 7, 13, 8), exits)
    print(theme, len(layers), "layers")

if __name__ == "__main__":
    build("study")
    build("arcade")
