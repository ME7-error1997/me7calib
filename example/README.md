# Example: Audi A4 1.8T

A complete session to try the app on: ten data logs from a 1.8T with 470 cc
injectors and an aftermarket turbo, the WinOLS export of its maps, the
profile that goes with them, and the workbook the current code produces.

| Path | What it is |
| --- | --- |
| `logs/` | ten ME7-Logger CSVs from one drive, about 25,000 rows in total |
| `maps/audi_a4_18t_maps.csv` | WinOLS export with KFLDIMX, KFLDRL, KFVPDKSD, FKKVS, KFZW, KFPBRK, KFPBRKNW, KFPRG and KFURL |
| `profile.json` | logger variable names, pre-processing rules, parameters, and the axes and factory maps imported from the export |
| `expected_ME_Tuning_Maps.xlsx` | the result the current code gives for these inputs |

The export has no KFFWL or KFFWLW, so the warm-up generator reports missing
axes and is skipped. Everything else runs.

## Walk-through

Start the app from the repository root, with `python -m me7calib` or
`run.bat`. The paths in the profile are relative to that root.

1. **ECU Profile**: *Load Existing Profile* and pick `example/profile.json`.
   The status table turns green straight away because the profile already
   carries the imported maps. *Import maps* re-reads the export from
   `maps/audi_a4_18t_maps.csv` and gives the same result; two rows show
   *Size Auto-Transposed*, which is the orientation healing for maps WinOLS
   writes with RPM on the x axis.
2. **Data Ingestion & Filtering**: browse to `example/logs` as the raw log
   folder and import with the parameters as loaded. Expect about 23,200
   rows after the transient filter, of which about 7,000 are wide open and
   2,000 are below the warm-up temperature. A copy of the profile is written
   into the logs folder as `Used_ECU_Profile.json`; git ignores it.
3. **Calculate**: run all. Ten blocks are calculated, warm-up is skipped.
   The console notes that VVT is disabled, so KFURL and KFPRG come out as a
   single column, and that one RPM bin had its KFPRG intercept anchored to
   20 hPa.
4. Save the workbook and compare it with the expected one:

```bash
python tools/compare_excel.py <your workbook>.xlsx example/expected_ME_Tuning_Maps.xlsx
```

A clean run prints `IDENTICAL within tolerance`.

To see what the sample-weight blocks are for, raise *Min samples per cell*
to 3 on the ingestion tab and calculate again: cells whose weight falls
below that are left blank instead of carrying single-sample noise.
