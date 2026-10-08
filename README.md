# ME7 Calib

Log-driven map calibration for Bosch ME7 engine controllers. Feed it a folder
of data logs and a WinOLS export of the factory maps; it fits corrected maps
onto the binary's own axes and writes them to an Excel workbook laid out cell
for cell like WinOLS, ready to paste back.

## What it calculates

| Area | Maps | From |
| --- | --- | --- |
| Boost control | KFLDIMX, KFLDRL, absolute wastegate duty | WOT rows: boost against RPM, duty against RPM and boost |
| Throttle handover | KFVPDKSD | WOT rows: base wastegate pressure and pressure ratio |
| Warm-up enrichment | KFFWL, KFFWLW, FKKVS_RL | warm-up rows: fuel trims against coolant temperature, load and RPM |
| Fuel trim | FKKVS | hot rows: fuel trims against RPM and injection time |
| Ignition | KFZW, KFZW2 | all rows: knock retard against RPM and load, split by VVT position |
| Intake manifold model | KFURL, KFPRG | all rows: linear fit of load against manifold pressure per RPM bin and VVT state |

Conventions: a positive fuel error means add fuel, and a corrected table is
the factory table times one plus the error. Trims can be logged as lambda
factors (1.05) or percent (5), selectable on the ingestion tab.

## Setup

Python 3.12 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Run

```bash
python -m me7calib
```

On Windows `run.bat` starts it without a console window.

Workflow, tab by tab:

1. **ECU Profile**: load a profile JSON or start from the defaults, check the
   logger column names against your logger, set the pre-processing rules,
   then import the WinOLS CSV export to pull in axes and factory values.
   Click a map row to view it.
2. **Data Ingestion & Filtering**: pick the folder of raw logs, adjust the
   parameters, and import. Logs are transient-filtered, time-aligned across
   files and split into Full, WOT, Warmup and Hot. A copy of the profile in
   use is saved next to the logs.
3. **Calculate**: run every generator, inspect each map and its sample
   weights, and save the Excel file. Each map block carries a twin block with
   the sample weight per cell, so thin data is visible before pasting.

### Logger channels

Default column names follow the ME7 variable names: `nmot_w`, `rl_w`,
`wdkba`, `pvdks_w`, `ps_w`, `ldtvm`, `wnwi_w`, `tevfakge_w`, `frm_w`,
`fra_w`, `tmotlin`, `pu`, `wkrm` and `TimeStamp`. Rename them on the profile
tab if your logger labels them differently. ME7-Logger and TunerPro CSV
layouts are read directly, including units and alias rows.

### WinOLS export

Export the maps listed above from WinOLS as a CSV: semicolon separated, one
map per line, with the axis values included. Maps that WinOLS writes with RPM
on the x axis are re-oriented on import. Missing maps are reported in the
status table; generators that need them are skipped, the rest still run.

### Profiles

A profile JSON holds the logger variable names, pre-processing rules, math
parameters, axes and factory base maps for one car. Older profile files with
upper-case keys load unchanged and are written back in the same spelling.

## Example

`example/` holds a complete session from an Audi A4 1.8T: ten logs, the
WinOLS export of its maps, a matching profile and the workbook the current
code produces from them. Its own README walks through the three tabs with it.

## Layout

| Package | Holds |
| --- | --- |
| `core/` | splatting, log ingestion, WinOLS parser, profile JSON, Excel export |
| `generators/` | the math per calibration area: boost, handover, warmup, fuel, ignition, manifold |
| `families/` | the ME7 declaration: defaults, target maps, log sources, generator list |
| `gui/` | PySide6 window and the three tabs, built from the family declaration |
| `tools/` | `compare_excel.py` compares two result workbooks block by block |

## Tests

```bash
pytest
```
