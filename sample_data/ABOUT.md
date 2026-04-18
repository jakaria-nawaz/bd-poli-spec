# Sample Data

This folder contains public sample files for the Bam-Dan Political Compass Survey.
It is the only data folder committed to this repository.

---

## What is in here

| File | Rows | Description |
|---|---|---|
| `questions_reference.csv` / `.parquet` | 22 | Complete question list — ID, category, Bengali original, English translation. No personal data. |
| `survey_with_scores_sample.csv` / `.parquet` | 100 | First 100 rows of the anonymised survey dataset, including computed scores and political label. |
| `findings.md` | — | Auto-generated summary of key findings from the full dataset (17,259 responses). |

---

## What is NOT in here

The full response dataset (17,259 rows) is not published in this repository.
It is fetched privately from Firebase using `fetch_data.py` and stored locally in `data/` (gitignored).

The complete private analysis outputs — charts, tables, and full CSV/Parquet exports — live in `private_analysis/` (also gitignored).

---

## Privacy

The sample rows contain no personally identifiable information. The following fields were excluded from all exports:

- `emailOrFacebook`
- `meta_ip`, `meta_isp`, `meta_city`, `meta_region`, `meta_country`
- `meta_userAgent`
- `doc_id`
- `q_101` through `q_105` (demographic duplicates collected within the survey)

Remaining fields (`age`, `gender`, `education`, `occupation`, `probashi`, `createdAt`, `meta_platform`, `meta_language`) are self-reported demographic categories — no free-text, no contact information.

---

## Join key

`question_id = N` in `questions_reference` maps to column `q_N` in the survey file.

Answer values use a 5-point Likert scale:

| Value | Meaning |
|---|---|
| −2 | Strongly disagree |
| −1 | Disagree |
| 0 | No opinion |
| +1 | Agree |
| +2 | Strongly agree |

---

## Full findings

See [findings.md](findings.md) for the key findings derived from all 17,259 responses.

> **Sample caveat:** The full dataset is a self-selected online sample — 88.7% male, 69% students — collected primarily via Facebook in April 2026. Findings describe Bangladesh's politically engaged online youth, not the general population.
