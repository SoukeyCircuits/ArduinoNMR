# Arduino NMR 5.2

KiCad hardware design (schematics + PCB) for the Arduino NMR 5.2 project.

## Layout

- `Arduino_NMR_5.2.kicad_pro` / `.kicad_sch` / `.kicad_pcb` — main KiCad project, schematic, and board
- `*.kicad_sch` — subsystem schematic sheets (amplifier, power, filters, TRX DUO, PHA 13HLN, Arduino Giga)
- `Arduino.pretty/` — custom PCB footprint library
- `Arduino.kicad_sym`, `New_Library.kicad_sym` — custom schematic symbol libraries
- `production/` — fabrication outputs (BOM, positions, designators, netlist, Gerber archive)

## Opening the project

Requires [KiCad](https://www.kicad.org/) 7 or later. Open `Arduino_NMR_5.2.kicad_pro`.
