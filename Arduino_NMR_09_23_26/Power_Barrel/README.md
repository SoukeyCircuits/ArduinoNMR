# Power_Barrel

Barrel-jack version of the Power-USBC board. The PD negotiation and interlock are gone. It takes a DC input on J1 (PJ-058B), makes the +8 V (BD80GC0VEFJ-ME2) and +3.3 V (BD33GA5WEFJ-E2) rails, and feeds the main board over the same J2 (1×12) and J4 (2×5 right-angle) connectors.

| File | What |
|---|---|
| `BOM_Barrel_09_23_26.csv` | every part: JLCPCB assembly, hand solder, and off-board items |
| `Barrel_Power_schematic.pdf` | the schematic |
| `KiCad_Files/Barrel_Power.kicad_pro` | open this in KiCad 10 |
| `KiCad_Files/production/1_jlcpcb_assembly.csv` + `_cpl.csv` | the files to upload to JLCPCB |

## Status

**Not yet built or ordered.** The input voltage range hasn't been confirmed against the regulators; check the BD80 dropout before choosing a supply. IC25 is out of stock at JLC, so hand solder it.
