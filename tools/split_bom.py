#!/usr/bin/env python3
"""Split Arduino_NMR_5.4 into four build lists.

  1  JLCPCB assembly   - front-side SMD the machine places
  2  hand solder, back - everything on the back side
  3  hand solder, front- THT connectors, RF shields, filter L/C, diode, jumpers
  4  external parts    - not on the PCB

Assignments below are explicit so they can be audited and edited.
Run from the project root:  python3 tools/split_bom.py
"""
import collections, csv, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "bom"; OUT.mkdir(exist_ok=True)

FILTER_L_NOTE = ("Filter inductor - choose value to suit the required filtering. "
                 "If filtering is done after the board, replace with a 0 ohm jumper resistor (0805).")
FILTER_C_NOTE = ("Filter capacitor - choose value to suit the required filtering. "
                 "If filtering is done off-board, DNP. Do NOT bridge with 0 ohm jumper resistors.")

ASSIGN = {
  # ref: (bucket, category, note, supplier, link)
  **{r: ("front", "Filter inductor", FILTER_L_NOTE, "", "") for r in
     "L13 L14 L16 L17 L18 L44 L45 L46 L47 L48 L49 L50 L51 L52 L53".split()},
  **{r: ("front", "Filter capacitor", FILTER_C_NOTE, "", "") for r in
     ("C62 C63 C67 C68 C69 C141 C142 C143 C144 C145 C146 C147 C148 C149 "
      "C150 C151 C152 C153 C154 C155").split()},
  **{r: ("front", "Connector (THT)", "Through-hole connector - hand solder.", "", "") for r in
     "J2 J7 J8 J11 J40 J41 J6".split()},
  **{r: ("back",  "Connector (THT)", "Through-hole connector on the BACK side - hand solder.", "", "") for r in
     "J4 J5 J10 J12".split()},
  **{r: ("front", "RF shield", "RF shield - hand solder after all other assembly.",
         "Mouser", "https://www.mouser.com/en/ProductDetail/388-MS329-10S") for r in
     "J16 J17 J32".split()},
  **{r: ("front", "Solder jumper", "PCB solder bridge - nothing to purchase; bridge by hand as required.", "", "")
     for r in "JP2 JP4 JP5 JP8".split()},
  **{r: ("back",  "Decoupling", "Back-side hand soldering.", "", "") for r in
     "C10 C17 C18 C19 C24 C29 C33 C39".split()},
  "C47": ("back", "Bulk cap (THT)", "Through-hole electrolytic on the BACK side - hand solder.", "", ""),
  "D1":  ("front", "Protection diode", "Protection diode - VALUE TBD, confirm before ordering. Hand solder.", "", ""),
  # L1, L2, L3, L15 are deliberately NOT here: L2/L15 are the LNA bias chokes
  # (+8V into IC13/IC14 RF-OUT/DC-IN) and L1/L3 are RF matching inductors.
  # None are filter elements - they stay on the JLC assembly list.
}


def pkg(fp):
    """Normalise KiCad chip-package names to the short form JLCPCB's matcher
    expects. Leaving 'C_0402_1005Metric' in the Footprint column makes JLC read
    the '1005' as 0402-metric and offer 01005 imperial parts - 1/6 the size."""
    m = re.match(r'^(?:C|R|L|LED|D)_(\d{4})_\d+Metric', fp)
    return m.group(1) if m else fp

def span(t, st):
    d=0; i=st; inq=esc=False
    while True:
        c=t[i]
        if esc: esc=False
        elif c=='\\': esc=True
        elif c=='"': inq=not inq
        elif not inq:
            if c=='(': d+=1
            elif c==')':
                d-=1
                if d==0: return i+1
        i+=1

s = (ROOT/"Arduino_NMR_5.4.kicad_pcb").read_text()
REF=re.compile(r'\(property "Reference" "([^"]*)"'); VAL=re.compile(r'\(property "Value" "([^"]*)"')
# same key names the Fabrication Toolkit accepts; only a bare Cnnn is a real code
LCSC=re.compile(r'\(property "(?:LCSC[^"]*|JLC[^"]*|MPN)" "([^"]*)"')
parts=[]
for m in re.finditer(r'\n\t\(footprint "([^"]*)"\n', s):
    b=s[m.start():span(s,m.start()+1)]
    r=REF.search(b)
    if not r or not r.group(1): continue    # skips the 4 mounting holes (empty Reference)
    # a footprint flagged BOTH exclude_from_bom and exclude_from_pos_files is a
    # board feature, not a part (mounting holes, fiducials) - skip it entirely
    _a = re.search(r'\n\t\t\(attr ([^)]*)\)', b)
    _a = _a.group(1) if _a else ""
    if "exclude_from_bom" in _a and "exclude_from_pos_files" in _a: continue
    # a footprint with an empty library id is board-local geometry (mounting
    # holes, fiducials), never a library part - exclude regardless of flags
    if not m.group(1).strip(): continue
    v=VAL.search(b); attr=re.search(r'\n\t\t\(attr ([^)]*)\)', b)
    lay=re.search(r'\n\t\t\(layer "([^"]+)"\)', b).group(1)
    lc=LCSC.search(b); code=lc.group(1) if lc else ""
    # accept a bare LCSC code (C114481) or a manufacturer part number
    # (0805W8F1001T5E); reject free-text notes, which always contain spaces
    if code and not re.fullmatch(r'[A-Za-z0-9._/#+-]{3,40}', code): code=""
    parts.append(dict(ref=r.group(1), val=v.group(1) if v else "",
        fp=pkg(m.group(1).split(":")[-1]), side="back" if lay.startswith("B.") else "front",
        attr=attr.group(1) if attr else "", lcsc=code))

def route(p):
    if p["ref"] in ASSIGN: return ASSIGN[p["ref"]][0]
    return "back" if p["side"]=="back" else "jlc"

rows=collections.defaultdict(list)
for p in parts:
    b=route(p)
    cat,note,sup,link = ASSIGN.get(p["ref"], (None,"","",""))[1:] if p["ref"] in ASSIGN else ("","","","")
    rows[b].append({**p, "cat":cat, "note":note, "sup":sup, "link":link})

def group_write(name, items, cols):
    g=collections.defaultdict(list)
    for r in items: g[(r["val"], r["fp"], r["cat"], r["note"], r["sup"], r["link"], r["lcsc"])].append(r["ref"])
    out=[]
    for (val,fp,cat,note,sup,link,lcsc),refs in g.items():
        refs=sorted(refs, key=lambda x:(re.sub(r'\d','',x), int(re.sub(r'\D','',x) or 0)))
        out.append({"Comment":val,"Designator":", ".join(refs),"Footprint":fp,"Quantity":len(refs),
                    "Category":cat,"Notes":note,"Supplier":sup,"Supplier Part # / Link":link,"LCSC Part #":lcsc})
    out.sort(key=lambda r:(r["Category"], r["Comment"]))
    with open(OUT/name,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for r in out: w.writerow({c:r.get(c,"") for c in cols})
    return len(out), sum(r["Quantity"] for r in out)

C_FULL=["Comment","Designator","Footprint","Quantity","Category","Notes","Supplier","Supplier Part # / Link"]
print(f"{'file':<32}{'lines':>6}{'parts':>7}")
for name,b,cols in [("1_jlcpcb_assembly.csv","jlc",["Comment","Designator","Footprint","Quantity","LCSC Part #"]),
                    ("2_handsolder_back.csv","back",C_FULL),
                    ("3_handsolder_front.csv","front",C_FULL)]:
    l,n=group_write(name, rows[b], cols); print(f"  {name:<30}{l:>6}{n:>7}")

EXT=[("Aluminium enclosure","",1,"Amazon","https://www.amazon.com/dp/B012SYN4OO",""),
     ("M3 standoffs","Assorted M3 standoff kit",1,"AliExpress","https://www.aliexpress.us/item/3256808109877301.html",""),
     ("Arduino Giga R1 WiFi","ABX00063 - board only",1,"Amazon","https://www.amazon.com/dp/B0BTTRZ9TB","Alternative with display: https://www.amazon.com/dp/B0G1L5C7MG"),
     ("USB-C power supply","",1,"Amazon","https://www.amazon.com/dp/B0CYZHY7BX",""),
     ("USB-C cable","",1,"Amazon","https://www.amazon.com/dp/B0CJY9PRNY","Alternative: https://www.amazon.com/dp/B0BLYXSTSQ"),
     ("SMA connectors","SMA-KWE 17 mm, 50 pcs",1,"AliExpress","https://www.aliexpress.us/item/3256808128195000.html","Mates with the board SMA footprints"),
     ("2.54 mm header pins","40P strip, cut to size",1,"AliExpress","https://www.aliexpress.us/item/3256806907643797.html",""),
     ("Heat sink - LNA","",0,"","","TBD"),
     ("Enclosure fan","",0,"","","TBD"),
     ("0 ohm jumper resistors 0805","Only if filtering is done off-board - see filter inductor note",0,"","","")]
with open(OUT/"4_external_parts.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Item","Description","Qty","Supplier","Link","Notes"])
    for r in EXT: w.writerow(r)
print(f"  {'4_external_parts.csv':<30}{len(EXT):>6}{'':>7}")
tot=sum(len(rows[b]) for b in ("jlc","back","front"))
print(f"\nreconciliation: {tot} placed parts + 4 mounting holes = {tot+4} of 130 footprints")

# ---- placement files -------------------------------------------------------
# Positions come from the Fabrication Toolkit's production/positions.csv, not
# from the board directly: the toolkit applies JLCPCB's per-package rotation
# and offset corrections (AUTO TRANSLATE), which must not be re-derived here.
POS = ROOT / "production" / "positions.csv"
if POS.exists():
    src = {r["Designator"].strip(): r
           for r in csv.DictReader(open(POS, encoding="utf-8-sig"))}
    def cpl(name, bucket, jlc_format):
        refs = [p["ref"] for p in rows[bucket]]
        have = [r for r in refs if r in src]
        cols = (["Designator","Mid X","Mid Y","Layer","Rotation"] if jlc_format
                else ["Designator","Value","Footprint","Side","Mid X","Mid Y","Rotation"])
        with open(OUT/name,"w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
            for r in sorted(have, key=lambda x:(x[0], int(''.join(c for c in x if c.isdigit()) or 0))):
                s_=src[r]; p_=next(q for q in rows[bucket] if q["ref"]==r)
                base={"Designator":r,"Mid X":s_["Mid X"],"Mid Y":s_["Mid Y"],
                      "Layer":s_["Layer"],"Rotation":s_["Rotation"]}
                if not jlc_format:
                    base={**base,"Value":p_["val"],"Footprint":p_["fp"],"Side":s_["Layer"]}
                w.writerow({c:base.get(c,"") for c in cols})
        return len(have), len(refs)
    for nm,bk,jf in [("1_jlcpcb_assembly_cpl.csv","jlc",True),
                     ("2_handsolder_back_placement.csv","back",False),
                     ("3_handsolder_front_placement.csv","front",False)]:
        h,t = cpl(nm,bk,jf)
        flag = "" if h==t else f"   <-- {t-h} MISSING from positions.csv"
        print(f"  {nm:<34}{h:>6}/{t}{flag}")
else:
    print("  production/positions.csv not found - re-run the Fabrication Toolkit")
