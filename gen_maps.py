#!/usr/bin/env python3
"""Generate tileset.png, genkan.tmj (tutorial entry) and commons.tmj (main MVP map)."""
import json, os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
TILE = 32; COLS_TS = 4; ROWS_TS = 4

palette = {
    1:("#D8D3C8","floorLight"),2:("#CCC5B8","floorDark"),3:("#4A3F35","wall"),
    4:("#9AA86C","tatami"),5:("#A9744F","wood"),6:("#C73E3A","stageRed"),
    7:("#EFE6D4","hubPaper"),8:("#B9C6E3","demoBlue"),9:("#B497C9","karaokePurple"),
    10:("#BDBDC4","silentGrey"),11:("#A8C3A0","boardGreen"),12:("#F0C75E","startGold"),
    13:("#C4BEB2","corridor"),14:("#8A2F2B","toriiRed"),15:("#2E2A33","inkDark"),16:("#EAD9A9","lantern"),
}
img = Image.new("RGBA",(COLS_TS*TILE,ROWS_TS*TILE),(0,0,0,0)); d = ImageDraw.Draw(img)
for gid,(hexc,name) in palette.items():
    i=gid-1; x0=(i%COLS_TS)*TILE; y0=(i//COLS_TS)*TILE
    d.rectangle([x0,y0,x0+TILE-1,y0+TILE-1],fill=hexc)
    if name=="wall":
        d.rectangle([x0,y0,x0+TILE-1,y0+6],fill="#5E5044"); d.line([x0,y0+TILE-1,x0+TILE-1,y0+TILE-1],fill="#332B24")
    elif name=="tatami":
        d.rectangle([x0,y0,x0+TILE-1,y0+TILE-1],outline="#7E8C52"); d.line([x0+16,y0+2,x0+16,y0+29],fill="#7E8C52")
    elif name=="wood":
        for k in range(0,TILE,8): d.line([x0,y0+k,x0+TILE-1,y0+k],fill="#8F5F3F")
    elif name=="toriiRed":
        d.rectangle([x0+4,y0+4,x0+27,y0+8],fill="#B34A44"); d.rectangle([x0+8,y0+8,x0+11,y0+27],fill="#B34A44"); d.rectangle([x0+20,y0+8,x0+23,y0+27],fill="#B34A44")
    elif name=="startGold":
        d.polygon([(x0+16,y0+6),(x0+26,y0+16),(x0+16,y0+26),(x0+6,y0+16)],outline="#8A6D2F")
    elif name=="lantern":
        d.ellipse([x0+8,y0+6,x0+24,y0+26],outline="#B98A2E")
img.save(f"{OUT}/tileset.png")

def tileset():
    return [{"columns":COLS_TS,"firstgid":1,"image":"tileset.png","imageheight":ROWS_TS*TILE,
        "imagewidth":COLS_TS*TILE,"margin":0,"name":"kanji-commons-placeholder","spacing":0,
        "tilecount":COLS_TS*ROWS_TS,"tileheight":TILE,"tilewidth":TILE,
        "tiles":[{"id":2,"properties":[{"name":"collides","type":"bool","value":True}]}]}]

def props(d_):
    return [{"name":k,"type":("bool" if isinstance(v,bool) else "string"),"value":v} for k,v in d_.items()]

class MapBuilder:
    def __init__(self,W,H):
        self.W,self.H=W,H; self.layers=[]; self.lid=1
    def empty(self): return [0]*(self.W*self.H)
    def fill(self,layer,x0,y0,x1,y1,gid):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): layer[y*self.W+x]=gid
    def tl(self,name,data,p=None,opacity=1.0):
        l={"data":data,"height":self.H,"width":self.W,"id":self.lid,"name":name,
           "opacity":opacity,"type":"tilelayer","visible":True,"x":0,"y":0}
        if p: l["properties"]=props(p)
        self.lid+=1; self.layers.append(l)
    def og(self,name):
        self.layers.append({"draworder":"topdown","id":self.lid,"name":name,"objects":[],
            "opacity":1,"type":"objectgroup","visible":True,"x":0,"y":0}); self.lid+=1
    def dump(self,path,mapprops):
        m={"compressionlevel":-1,"height":self.H,"width":self.W,"infinite":False,
           "layers":self.layers,"nextlayerid":self.lid,"nextobjectid":1,"orientation":"orthogonal",
           "renderorder":"right-down","tiledversion":"1.10.2","tileheight":TILE,"tilewidth":TILE,
           "type":"map","version":"1.10","properties":props(mapprops),"tilesets":tileset()}
        json.dump(m,open(path,"w"),indent=1)
        for l in m["layers"]:
            if l["type"]=="tilelayer": assert len(l["data"])==self.W*self.H,(path,l["name"])
        return m

# ---------------- GENKAN (tutorial entry, 16x10) ----------------
g=MapBuilder(16,10)
floor=g.empty(); g.fill(floor,0,0,15,9,7)               # paper floor
g.fill(floor,1,4,3,6,4)                                  # tatami spawn nook
walls=g.empty(); g.fill(walls,0,0,15,0,3); g.fill(walls,0,9,15,9,3)
for y in range(10): walls[y*16+0]=3; walls[y*16+15]=3
start=g.empty(); g.fill(start,1,4,2,6,12)
z_lang_en=g.empty(); g.fill(z_lang_en,5,2,6,3,8)
z_lang_ja=g.empty(); g.fill(z_lang_ja,5,6,6,7,6)
z_bubble=g.empty(); g.fill(z_bubble,8,3,10,6,11)
z_exit=g.empty(); g.fill(z_exit,14,4,14,5,14)
g.tl("floor",floor)
g.tl("zone/lang-en",z_lang_en,opacity=0.5)
g.tl("zone/lang-ja",z_lang_ja,opacity=0.5)
g.tl("zone/bubble-demo",z_bubble,{"jitsiRoom":"kanji-commons-genkan-circle"},opacity=0.4)
g.tl("exit-to-commons",z_exit,{"exitUrl":"./commons.tmj"},opacity=0.6)
g.tl("walls",walls); g.og("floorLayer"); g.tl("start",start,opacity=0.6)
g.dump(f"{OUT}/genkan.tmj",{
    "script":"../scripts/genkan.js","mapName":"Kanji Commons — Genkan (entry & tutorial)",
    "mapDescription":"Small enclosed entry room: pick a language, learn to move and talk, then step through the torii to the commons."})

# ---------------- COMMONS (30x20 quadrants) ----------------
c=MapBuilder(30,20); W,H=30,20
floor=c.empty()
for y in range(H):
    for x in range(W): floor[y*W+x]=1 if (x+y)%2==0 else 2
c.fill(floor,0,9,W-1,9,13)
for y in range(H): floor[y*W+14]=13
c.fill(floor,1,1,13,8,5)      # stage: wood
c.fill(floor,15,1,28,8,7)     # library: paper
c.fill(floor,1,10,13,18,4)    # breakout: tatami
c.fill(floor,23,13,27,17,9)   # karaoke corner
walls=c.empty(); c.fill(walls,0,0,W-1,0,3); c.fill(walls,0,H-1,W-1,H-1,3)
for y in range(H): walls[y*W+0]=3; walls[y*W+(W-1)]=3
for x in range(1,W-1):
    if x not in (6,7,14,21,22): walls[9*W+x]=3
for y in range(1,H-1):
    if y not in (4,5,9,13,14): walls[y*W+14]=3
start=c.empty()
for sx,sy in [(14,9),(13,9),(15,9)]: start[sy*W+sx]=12
def z(x0,y0,x1,y1,gid):
    l=c.empty(); c.fill(l,x0,y0,x1,y1,gid); return l
c.tl("floor",floor)
c.tl("zone/stage",z(2,2,12,7,6),{"jitsiRoom":"kanji-commons-stage"},0.35)
c.tl("zone/breakout",z(2,11,12,17,4),{"jitsiRoom":"kanji-commons-breakout-1"},0.35)
c.tl("zone/library",z(22,2,27,6,11),{"openWebsite":"../web/library.html","openWebsiteTrigger":"onaction",
    "openWebsiteTriggerMessage":"Press SPACE to open the Library","openWebsiteWidth":"60"},0.35)
c.tl("zone/kanji-demo",z(16,2,20,6,8),{"openWebsite":"../web/kanji-quiz.html","openWebsiteTrigger":"onaction",
    "openWebsiteTriggerMessage":"Press SPACE: kanji quiz demo (live dictionary API)","openWebsiteWidth":"55"},0.35)
c.tl("zone/tracing",z(16,7,20,8,8),{"openWebsite":"../web/tracing.html","openWebsiteTrigger":"onaction",
    "openWebsiteTriggerMessage":"Press SPACE: stroke-order tracing kiosk (KanjiVG)","openWebsiteWidth":"55"},0.35)
c.tl("zone/silent-reading",z(22,7,27,8,10),{"silent":True},0.35)
c.tl("zone/common-board",z(16,11,20,14,11),{"openWebsite":"../web/board.html","openWebsiteTrigger":"onaction",
    "openWebsiteTriggerMessage":"Press SPACE to read the common-room board","openWebsiteWidth":"55"},0.35)
c.tl("zone/karaoke",z(23,13,27,17,9),{"jitsiRoom":"kanji-commons-karaoke","openWebsite":"../web/karaoke.html",
    "openWebsiteTrigger":"onaction","openWebsiteTriggerMessage":"Press SPACE to open the karaoke corner","openWebsiteWidth":"55"},0.35)
c.tl("exit-to-genkan",z(14,1,14,1,14),{"exitUrl":"./genkan.tmj"},0.6)
c.tl("walls",walls); c.og("floorLayer"); c.tl("start",start,opacity=0.6)
m=c.dump(f"{OUT}/commons.tmj",{
    "script":"../scripts/commons.js","mapName":"Kanji Commons — MVP campus",
    "mapDescription":"Stage, breakout, common room with karaoke corner, and library with live kanji kiosks."})
print("OK:",[l["name"] for l in m["layers"]])
