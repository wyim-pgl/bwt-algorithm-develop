# Figure outputs

Figure 1 uses the completed native period-100 P/B/F/H runs at detection
commit `0363d8b` (jobs 6141841_0 and 6143150_1..3).
`figure_curve_data.csv` contains their numeric scores plus the fixed competitor
baselines; `figure_curve.png` and `.pdf` are deposited. The earlier
6129408 attempt failed at startup and is superseded. The full-range
identity sweep is separately deposited under `regen/` (job 6143151_0..4)
for Supplementary Table S3; it does not supply this P/B/F/H curve.

To render the active curve from the scored CSV:

```bash
python3 results/figures/make_curve_figure.py
```

The CSV must contain the columns `series,label,region_recall,region_precision,`
`bp_recall,bp_precision`, with BWTandem rows P/B/F/H and competitor rows ULTRA,
tantan, TRF and TRASH. The renderer validates the complete schema, labels and
0--100 numeric range before importing matplotlib or creating output files.
The checked-in CSV has four BWTandem and four competitor rows.
The composed manuscript figure set is under `paper_figs/`; see its README.

Files containing `superseded` preserve the withdrawn earlier-build curve for
audit history only.  They are not manuscript inputs.  The superseded renderer
writes only superseded filenames, so running it cannot recreate an apparently
active Figure 1.
