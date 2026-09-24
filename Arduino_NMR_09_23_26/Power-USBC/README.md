# Power-USBC

USB-C PD power board for the Arduino NMR. It negotiates a fixed 9 V from any USB-C PD supply (HUSB238A-BB001), makes the +8 V (LNA) and +3.3 V rails on board, and feeds them to the main board over J2 (1×12) and J4 (2×5 right-angle).

- **Over-voltage interlock:** a TL431A cuts the input if the supply ever delivers more than ~10 V.
- **Indicators:** LED1–LED3 show +9V_SYS, +8V and +3V3.
- **2 layers, 1.6 mm.**

| File | What |
|---|---|
| `BOM_USBC_09_23_26.csv` | every part: JLCPCB assembly, hand solder, and off-board items |
| `USBC_Power_schematic.pdf` | the schematic |
| `KiCad_Files/usbc-power.kicad_pro` | open this in KiCad 10 |
| `KiCad_Files/production/1_jlcpcb_assembly.csv` + `_cpl.csv` | the files to upload to JLCPCB |

## Known issues

- **The R23 failsafe is in the schematic but not on the PCB.** The schematic has R23 and R32 at 6.04k in parallel, so a single failed resistor gives 12 V (caught by the interlock) instead of 28 V. The PCB and BOM still have a single 3.00k R23. Run *Update PCB from Schematic* before the next order.
- **J10 (USB-C receptacle):** JLC doesn't stock the GCT USB4105-GF-A-120 (48 V). Either hand solder it or switch to the HRO TYPE-C-31-M-12 (C165948), which is rated 20 V only.
- **IC25 (BD33GA5WEFJ-E2)** is out of stock at JLC. Hand solder it.
- **D20 (SMAJ24A)** clamps at 38.9 V, which is above U20's 33 V absolute maximum. Acceptable for a test board.
