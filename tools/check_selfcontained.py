#!/usr/bin/env python3
"""Fail if any footprint reference points outside the project's own libraries.

Run before pushing. Catches the usual regression: a part added from KiCad's
global library chooser arrives as e.g. "Capacitor_SMD:C_0402_1005Metric",
which resolves on this machine and nowhere else.

    python3 tools/check_selfcontained.py        # exit 1 on any external ref
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent

libs = {}
tbl = root / "fp-lib-table"
if not tbl.exists():
    sys.exit("no fp-lib-table")
for name, uri in re.findall(r'\(name "([^"]+)"\).*?\(uri "([^"]+)"\)', tbl.read_text()):
    if "${KIPRJMOD}" not in uri:
        print(f"  WARN  library {name!r} is not project-relative: {uri}")
    libs[name] = root / uri.replace("${KIPRJMOD}/", "")

refs = {}
files = [f for f in sorted(root.glob("*.kicad_sch")) + sorted(root.glob("*.kicad_pcb"))
         if not f.name.startswith(("_autosave-", "_recovered"))]
for f in files:
    txt = f.read_text()
    pats = [r'\(property "Footprint" "([^"]+)"']
    if f.suffix == ".kicad_pcb":
        pats.append(r'\n\t\(footprint "([^"]+)"')
    for p in pats:
        for fid in re.findall(p, txt):
            refs.setdefault(fid, set()).add(f.name)

external, missing = [], []
for fid, where in sorted(refs.items()):
    lib, _, name = fid.rpartition(":")
    if not lib:
        external.append((fid, "no library prefix", where)); continue
    if lib not in libs:
        external.append((fid, f"library {lib!r} not in fp-lib-table", where)); continue
    if not (libs[lib] / f"{name}.kicad_mod").exists():
        missing.append((fid, f"not found in {libs[lib].name}", where))

for group, label in ((external, "EXTERNAL / UNDECLARED"), (missing, "DECLARED BUT MISSING")):
    if group:
        print(f"\n{label}:")
        for fid, why, where in group:
            print(f"  {fid}\n      {why}\n      in: {', '.join(sorted(where))}")

total = len(refs)
bad = len(external) + len(missing)
print(f"\n{total - bad}/{total} footprint references resolve inside the project")
sys.exit(1 if bad else 0)
