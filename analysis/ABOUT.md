# Community Analysis

This folder contains publicly committed analysis outputs — charts and data tables — contributed by the project team or the community. Everything here is safe to share and is tracked in version control.

---

## What belongs here

- Charts and tables derived from the anonymised sample (`sample_data/`) or from the full dataset with results already aggregated (no row-level data)
- Jupyter notebooks or Python scripts that reproduce a specific finding
- Any additional breakdowns or visualisations that add public value

If your analysis requires the full 17,259-row dataset, run it locally and only commit the aggregated output (chart or summary table) here — not the raw rows.

---

## Files in this folder

| File | Description |
|---|---|
| `probashi_comparison.png` / `.csv` | Home vs diaspora (probashi) mean scores across all 22 questions |
| `occupation_scores.png` / `.csv` | Economic scores and key question means broken down by occupation |
| `daily_growth.png` / `.csv` | Daily and cumulative response counts over the collection period |

---

## Contributing

1. Fork the repository and create a branch.
2. Add your chart, table, or notebook to this folder with a descriptive filename (no numeric prefix — use `topic_description.ext` style).
3. Update the table above in this file.
4. Open a pull request with a short description of what the analysis shows.

See the project [README](../README.md) for data format details and the join key between questions and survey columns.

---

## Privacy reminder

Do not commit any file that contains row-level survey data. Only aggregated outputs (means, counts, percentages, charts) belong here. If in doubt, check [sample_data/ABOUT.md](../sample_data/ABOUT.md) for the field exclusion list.
