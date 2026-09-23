# Changelog

All notable changes to the Arduino Giga NMR spectrometer board.

Revisions are dated by the folder they were developed in. Part counts are
footprints carrying a reference designator, excluding mounting holes.

---

## [5.4] — 2026-09-22 — *sent to production*

The power supply left the board. Everything that generated a rail now lives on
a separate 2-layer USB-C PD board, and this board receives its rails over a
connector instead.

**126 parts** (was 108) · 4 layers · 120 × 79 mm

### Removed — on-board power generation

| Ref | Part | Was |
|---|---|---|
| J1 | `PJ-058B` | barrel jack input |
| IC6 | `BD50GC0VEFJ-ME2` | +5 V regulator |
| IC7 | `BD80GC0VEFJ-ME2` | +8 V regulator (LNA rail) |
| IC25 | `BD33GA5WEFJ-E2` | +3.3 V regulator |
| C11, C12, C21, C22, C23, C26, C32, C42 | 10 nF etc. | regulator decoupling |
| IC9 | `PE4251MLI-Z` | one RF switch |

### Added — inter-board connectors

- **J2** — 1×12 header, carrying +8V, +3V3, VIN and the control/TTL lines
- **J7** — 1×05 header
- **R18** — 50 Ω

### Added — RF filter bank

Sixteen capacitors (C63, C67–C69, C142–C155) and ten inductors (L14, L16–L18,
L45–L46, L48–L53) forming an LC ladder in the receive path. Values are chosen
per build; if filtering is done off-board the inductors become 0 Ω jumpers and
the capacitors are left unpopulated.

### Changed

- **C43** 1 pF → 100 nF

### Repository and tooling

- All footprints consolidated into `Arduino_NMR.pretty` (54), so a fresh clone
  resolves without the author's personal library table
- Recovered `L_0805_2012Metric_Pad1.15x1.40mm_HandSolder`, which KiCad 10
  dropped from its stock library, from the board itself
- 261 footprint references repointed; dead `Library` entry removed from
  `fp-lib-table`
- `tools/split_bom.py` — splits the board into JLCPCB assembly (63), back-side
  hand solder (13), front-side hand solder (50) and off-board parts, with
  matching placement files
- `tools/check_selfcontained.py` — pre-push guard, passes 32/32
- Six sheets not in the hierarchy moved to `archive/`

---

## [5.2] — 2026-06 — *baseline*

**108 parts** · 4 layers. Self-powered from a barrel jack, with on-board +5 V,
+8 V and +3.3 V regulators and six RF switches.

---

## Companion boards

Developed alongside 5.4 and sent to production the same day, in their own
repositories:

- **usbc-power 1.0** — 9 V USB-C PD sink (HUSB238A-BB001) with the +8 V and
  +3.3 V regulators moved across from this board, plus a TL431A hardware
  over-voltage interlock
