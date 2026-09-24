# License — this footprint library

The 11 footprints in this directory are **verbatim copies** of footprints from the
official KiCad footprint libraries, copied here so this project is self-contained.

They remain the work of the KiCad Library team and their contributors, and are licensed
under **Creative Commons CC-BY-SA 4.0 with the KiCad library exception**:

> To the extent that the creation of electronic designs that use "Licensed Material" can
> be considered to be "Adapted Material", then the copyright holder waives article 3 of
> the license with respect to these designs and any generated files which use data
> provided as part of the "Licensed Material."

Source: <https://www.kicad.org/libraries/license/>

## What that means here

- **Designs made with these footprints are not encumbered.** The exception waives the
  ShareAlike clause for the designs themselves. Arduino_NMR_5.4 can be licensed however
  its author chooses — proprietary, closed, commercial, anything.
- **This directory is a redistribution of the library itself**, which the exception does
  *not* cover. So this folder stays CC-BY-SA 4.0, with attribution, and this notice must
  travel with it.

Files here:

```
C_0402_1005Metric        C_0603_1608Metric      C_1206_3216Metric
D_SMA                    Diodes_PowerDI3333-8   LED_0805_2012Metric
QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias
R_0402_1005Metric        SOT-23
USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal
USB_C_Receptacle_HRO_TYPE-C-31-M-12
```

The `usbc-power.kicad_sym` symbol library in the parent directory is **not** covered by
this: the HUSB238A symbol was drawn from the Hynetek datasheet pinout, not copied from a
KiCad library.
