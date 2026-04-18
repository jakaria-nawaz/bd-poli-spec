# Bam-Dan Survey Analytics

Open analysis of the **Bam-Dan Political Compass Survey** — a self-selected online survey of Bangladeshi political opinions collected in April 2026 via [bam-dan.com](https://bam-dan.com).

17,259 responses. 22 policy questions. Two axes: economic (left ↔ right) and social (secular ↔ religious/conservative).

> **Sample caveat:** This is a self-selected online sample — 88.7% male, 69% students — collected primarily through Facebook. Findings describe Bangladesh's politically engaged online youth, not the general population.

---

## Key Findings

| Finding | Detail |
|---|---|
| Largest group | Centrist (47.9%) |
| Centrist illusion | 52.4% of self-labelled Centrists score left-of-centre economically |
| Biggest gender gap | Q16 — equal property rights (female mean +0.59 vs male −0.23, gap = 0.82) |
| Most agreed | Q17 — strict environmental rules for factories (mean = 1.40) |
| Most divisive | Q9 — laws should follow religious rules (std dev = 1.48, bimodal) |
| Generation surprise | Youth (18–24) stricter on religious speech than middle-aged (35–44) |
| Education effect | Strongest predictor of support for minority rights (Q21) |
| Peak day | 12,798 responses on April 10, 2026 |

Full narrative: [sample_data/findings.md](sample_data/findings.md)

---

## Project Structure

```
bam-dan-analytics/
│
├── fetch_data.py                   # Fetches from Firebase → data/
├── generate_export_files.py        # Builds anonymised exports → private_analysis/
├── generate_questions_reference.py # Builds question lookup → sample_data/
│
├── analysis.ipynb                  # Exploratory sanity checks
├── deep_analysis.ipynb             # Main publication-ready analysis (12 tasks)
├── question_level_analysis.ipynb   # Per-question crosstabs by demographic
│
├── requirements.txt
│
├── specs/
│   ├── 01_fetch_data.md            # Spec: Firebase fetch pipeline
│   ├── 02_data_analysis.md         # Spec: all 12 analysis tasks with chart styles
│   └── 03_data_exports.md          # Spec: export scripts, sample_data/, privacy rules
│
├── analysis/                       # ✅ Committed — public community analysis outputs
│   ├── ABOUT.md                    # How to contribute analysis
│   ├── probashi_comparison.png/csv # Home vs diaspora comparison
│   ├── occupation_scores.png/csv   # Economic scores by occupation
│   └── daily_growth.png/csv        # Response volume over time
│
├── sample_data/                    # ✅ Committed — safe public sample
│   ├── ABOUT.md                    # Explains what is and isn't in this folder
│   ├── findings.md                 # Key findings from the full 17,259-response dataset
│   ├── questions_reference.csv     # All 22 questions: ID, category, Bengali + English
│   ├── questions_reference.parquet
│   ├── survey_with_scores_sample.csv     # First 100 anonymised rows with scores
│   └── survey_with_scores_sample.parquet
│
├── data/                           # ❌ Gitignored — raw Firebase data, fetched locally
│   ├── responses.parquet
│   ├── metadata.parquet
│   ├── metadata.json
│   └── questions_v1.parquet
│
└── private_analysis/               # ❌ Gitignored — full exports and charts (create locally)
    ├── charts/                     # 10 publication-ready PNG charts (150 dpi)
    ├── tables/                     # 10 CSV tables matching each chart
    ├── findings.md
    ├── survey_anonymised.csv       # 17,259 rows, no scores
    ├── survey_anonymised.parquet
    ├── survey_with_scores.csv      # 17,259 rows + economicScore, socialScore, resultLabel
    └── survey_with_scores.parquet
```

---

## Survey Design

The survey presents 22 statements on a 5-point Likert scale:

| Value | Label (Bengali) | Meaning |
|---|---|---|
| −2 | একদমই একমত নই | Strongly disagree |
| −1 | একমত নই | Disagree |
| 0 | মতামত নেই | No opinion |
| +1 | একমত | Agree |
| +2 | পুরোপুরি একমত | Strongly agree |

Questions 1–8 and 17–18 feed the **economic score** (negative = left, positive = right).
Questions 9–16 and 19–22 feed the **social score** (negative = secular/liberal, positive = religious/conservative).

See [sample_data/questions_reference.csv](sample_data/questions_reference.csv) for the full question list with Bengali originals and English translations.

### Political Labels

| Label | Quadrant |
|---|---|
| Leftist | Economic left + Social secular |
| Center Left | Moderate economic left + Social secular |
| Centrist | Near-centre on both axes |
| Center Right | Moderate economic right + Traditional |
| Rightwing | Economic right + Traditional |
| Religious Left | Economic left + Religious/conservative |
| Religious Right | Economic right + Religious/conservative |

---

## Community Analysis

The `analysis/` folder is committed to the repository and is open for contributions. It holds aggregated charts and tables that are safe to share publicly — no row-level survey data.

| File | Description |
|---|---|
| `probashi_comparison.png` / `.csv` | Home vs diaspora mean scores across all 22 questions |
| `occupation_scores.png` / `.csv` | Economic scores and key question means by occupation |
| `daily_growth.png` / `.csv` | Daily and cumulative response counts over the collection period |

To contribute your own analysis, add a chart or summary table to `analysis/` and open a pull request. See [analysis/ABOUT.md](analysis/ABOUT.md) for contribution guidelines.

---

## Private Analysis

`private_analysis/` is gitignored and never committed. If you have Firebase credentials and want to run the full analysis locally, create this folder by running `deep_analysis.ipynb` — it will populate `private_analysis/charts/`, `private_analysis/tables/`, and `private_analysis/findings.md` automatically.

You can also use `private_analysis/` freely as a scratch space for your own local work without risk of accidentally committing sensitive data.

---

## Sample Data

The `sample_data/` folder is the only row-level data committed to this repo. It contains:

| File | Rows | Description |
|---|---|---|
| `questions_reference.csv` / `.parquet` | 22 | Complete question list — no personal data |
| `survey_with_scores_sample.csv` / `.parquet` | 100 | First 100 anonymised rows with scores and political label |
| `findings.md` | — | Key findings from the full dataset |

See [sample_data/ABOUT.md](sample_data/ABOUT.md) for details on what is excluded and why.

### Excluded fields (not in any export)

`emailOrFacebook`, `meta_ip`, `meta_isp`, `meta_city`, `meta_region`, `meta_country`, `meta_userAgent`, `doc_id` — PII or near-identifying.
`q_101` through `q_105` — demographic duplicates collected within the survey form.

---

## Setup

```bash
git clone https://github.com/your-org/bam-dan-analytics.git
cd bam-dan-analytics
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Reproducing the Analysis

### 1. Fetch fresh data (requires Firebase credentials)

You need a `serviceAccountKey.json` from the Firebase project. **Never commit this file.**

```bash
python fetch_data.py
```

Saves to `data/`: `responses.parquet`, `metadata.parquet`, `metadata.json`, `questions_v1.parquet`

### 2. Run the main analysis

Open `deep_analysis.ipynb` in Jupyter and run all cells:

```bash
jupyter notebook deep_analysis.ipynb
```

Saves 10 charts to `private_analysis/charts/`, 10 tables to `private_analysis/tables/`, and regenerates `private_analysis/findings.md`.

### 3. Regenerate full exports

```bash
python generate_export_files.py      # → private_analysis/survey_*.csv / .parquet
python generate_questions_reference.py  # → sample_data/questions_reference.*
```

### 4. Explore question-level breakdowns

Open `question_level_analysis.ipynb` for per-question crosstabs across gender, age, education, and political alignment.

---

## Charts

All charts are generated by `deep_analysis.ipynb` and saved to `private_analysis/charts/` (gitignored).

| # | File | Description |
|---|---|---|
| 01 | `01_political_distribution.png` | Share of respondents by political label |
| 02 | `02_centrist_illusion.png` | Scatter of Centrists on the two-axis compass |
| 03 | `03_gender_gap_questions.png` | Top 5 questions by male–female mean difference |
| 04 | `04_question_consensus.png` | All 22 questions ranked by mean and by divisiveness |
| 05 | `05_age_social_heatmap.png` | Social question means by age bracket |
| 06 | `06_education_tolerance.png` | Tolerance questions by education level |
| 07 | `07_divisive_distributions.png` | Full response distributions for 5 most divisive questions |
| 08 | `08_probashi_comparison.png` | Home vs diaspora (probashi) comparison across all 22 questions |
| 09 | `09_occupation_economics.png` | Economic scores and key questions by occupation |
| 10 | `10_growth_over_time.png` | Daily and cumulative response growth |

---

## Methodology Notes

- **Scoring:** Each question has a weight of +1 or −1. A respondent's economic (or social) score is the weighted sum of their answers on that axis, normalised to a −10 to +10 range.
- **Classification:** Political labels are assigned by combining the sign and magnitude of both scores with a standard deviation threshold (see [specs/02_data_analysis.md](specs/02_data_analysis.md) for the exact logic).
- **Statistical tests:** Gender and probashi comparisons use Welch's two-sample t-test (unequal variance). Significance threshold: p < 0.05.

---

## Contributing

This project is open for analysis contributions. If you spot an error in a translation, a chart, or a finding, please open an issue.

Code style: plain Python and pandas, no custom classes. Charts use matplotlib/seaborn. Notebooks follow the task structure defined in `specs/02_data_analysis.md`.

---

## License

Data and findings: [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
Code: [MIT License](https://opensource.org/licenses/MIT)

If you use this data or analysis in publication, please credit: **Bam-Dan Political Compass Survey, April 2026, bam-dan.com**
