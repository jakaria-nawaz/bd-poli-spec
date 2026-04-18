# Spec: Bam-Dan Survey — Data Analysis Notebook

## Goal
Produce analysis outputs — charts, tables, findings — that are:
- Interesting and shareable for Bangladeshi Facebook audiences
- Suitable as evidence for press articles (Daily Star, Prothom Alo, Business Standard)
- Honest about sample limitations throughout
- Publication-quality visuals (clean, styled, English labels only)

## Prerequisites
- `data/responses.parquet` exists (fetched via `fetch_data.py`)
- Virtual environment already set up and active

## New dependency to add to requirements.txt
```
scipy
```
`scipy` is needed for Task 9 (statistical significance testing on group differences).
Add this line to requirements.txt and run `pip install -r requirements.txt`.

---

## Data Context

### Columns available
Flat fields: `age`, `gender`, `education`, `occupation`, `probashi`,
`economicScore`, `socialScore`, `resultLabel`, `createdAt`

Question responses: `q_1` through `q_22` (Likert scale: -2 to +2)

Demographic duplicates stored as questions — exclude from all analysis:
`q_101` (gender), `q_102` (education), `q_103` (occupation),
`q_104` (probashi) — drop these columns before any analysis.

### Known data quality issues
- `district`: 100% null — skip all geographic analysis
- `meta_country`, `meta_city`, `meta_region`: ~94% null — skip
- `q_101` to `q_104`: duplicates of demographic fields — drop

### Sample profile (label every chart with this caveat)
- 17,259 total responses, April 3–17 2026
- 88.7% male (n=15,313), 10.3% female (n=1,781)
- 69% students, 18% service/employment
- 73.5% bachelor/masters or higher
- Self-selected Facebook audience — not nationally representative

---

## Classification Logic (combined mean + std_dev)

All tables that include a `classification` column must use this combined
logic — never mean alone. This prevents "Mixed" from hiding genuine
polarisation from non-technical readers.

```python
def classify_question(mean, std_dev):
    """
    Classify a question response using both mean (direction)
    and std_dev (how divided people are).
    Threshold for 'divided': std_dev >= 1.0
    """
    divided = std_dev >= 1.0  # True means people are split

    if mean > 1.0:
        return 'Strong consensus — agree' if not divided else 'Majority agree — but divided'
    elif mean >= 0.5:
        return 'Moderate agreement' if not divided else 'Leaning agree — but divided'
    elif mean >= -0.5:
        return 'Genuinely neutral' if not divided else 'Polarised — two opposing camps'
    elif mean >= -1.0:
        return 'Moderate disagreement' if not divided else 'Leaning disagree — but divided'
    else:
        return 'Strong consensus — disagree' if not divided else 'Majority disagree — but divided'
```

The most important label is **"Polarised — two opposing camps"** — this
applies when the mean looks neutral but std_dev is high. Q9 (laws follow
religion) and Q16 (equal property rights) both fall here. This is not
neutrality — it is two sides cancelling each other out.

Use `classify_question(mean, std_dev)` in every table that has a
classification column.

---

## Actual Question Text
(Real Bengali questions translated to English.
Use this mapping everywhere in the notebook.)

```python
QUESTION_TEXT = {
    1:  "State should control major industries & businesses",
    2:  "Business should be open to all — no govt interference",
    3:  "Tax the rich more to help the poor",
    4:  "Govt should not interfere in how businesses operate",
    5:  "Worker unions should be stronger",
    6:  "Foreign companies should get special incentives to invest",
    7:  "Education & healthcare should be completely free for all",
    8:  "Everyone has full rights over their own property",
    9:  "Laws should follow religious rules",
    10: "Religion is personal — state should treat all equally",
    11: "Traditional family & social norms matter more than modernity",
    12: "Society should not restrict what people wear or how they behave",
    13: "Religious education should be compulsory in schools",
    14: "Freedom of speech — even if it hurts someone",
    15: "Our culture must be protected from foreign influence",
    16: "Men and women should have equal property rights",
    17: "Strict rules & fines for factories to protect environment",
    18: "Some environmental damage is acceptable for economic growth",
    19: "State should equally support all religious festivals",
    20: "Strictly ban anything that hurts religious sentiments",
    21: "Indigenous/ethnic minorities deserve special rights & protection",
    22: "Same rules for everyone — no special treatment for any group",
}

QUESTION_CATEGORY = {
    1: 'economic', 2: 'economic', 3: 'economic', 4: 'economic',
    5: 'economic', 6: 'economic', 7: 'economic', 8: 'economic',
    9: 'social',  10: 'social',  11: 'social',  12: 'social',
    13: 'social', 14: 'social',  15: 'social',  16: 'social',
    17: 'economic', 18: 'economic',
    19: 'social', 20: 'social',  21: 'social',  22: 'social',
}
```

---

## Code Style Requirements
- Written for junior developers — every non-obvious line has a short comment
- Descriptive variable names (`mean_score_by_gender` not `df2`)
- No classes, no decorators, no unnecessary abstractions
- Each function does exactly one thing and has a docstring
- All outputs saved to `private_analysis/` folder (create if not exists)
- Bengali text must NOT appear in chart labels — causes render issues
  (boxes instead of text). Use English only in all matplotlib/seaborn output.

---

## Output Structure

```
private_analysis/
  charts/     <- PNG files, 150 dpi, white background
  tables/     <- CSV files
  findings.md <- Auto-generated key findings summary
```

`private_analysis/` is gitignored. It is a local working folder — never committed.
See `specs/03_data_exports.md` for files that ARE published (in `sample_data/`).

---

## Chart Style Rules (apply to every single chart)

```python
# Colour palette — use these consistently across all charts
COLORS = {
    'primary':  '#2C3E7A',  # deep navy
    'red':      '#E8442A',  # warm red
    'amber':    '#F5A623',  # amber
    'green':    '#27AE60',  # green
    'purple':   '#8E44AD',  # purple
    'blue':     '#2980B9',  # blue
    'light_bg': '#F0F4FF',  # chart background
    'text':     '#1A1A2E',  # dark text
    'muted':    '#5A5A7A',  # muted/subtitle text
}

# For political labels — always use these exact colours
LABEL_COLORS = {
    'Leftist':         '#C0392B',
    'Center Left':     '#E67E22',
    'Centrist':        '#F39C12',
    'Center Right':    '#2980B9',
    'Rightwing':       '#1A5276',
    'Religious Left':  '#8E44AD',
    'Religious Right': '#6C3483',
}

# Categorical colour list for multi-group charts
CAT_COLORS = ['#2C3E7A','#E8442A','#F5A623','#27AE60',
              '#8E44AD','#2980B9','#E67E22','#16A085']
```

Apply to every chart:
- Figure background: `facecolor='white'`
- Axes background: `#F0F4FF`
- Remove top and right spines on all bar/line charts
- Add sample caveat as figure subtitle on every chart:
  ```python
  fig.text(0.5, -0.02,
           'Self-selected online sample | n=17,259 | April 2026 | bam-dan.com',
           ha='center', fontsize=9, color='#5A5A7A', style='italic')
  ```
- Save with: `plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')`

---

## Analysis Tasks

---

### Task 1: Setup Cell

```python
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings

warnings.filterwarnings('ignore')
matplotlib.use('Agg')

# Create output directories if they do not exist
os.makedirs('private_analysis/charts', exist_ok=True)
os.makedirs('private_analysis/tables', exist_ok=True)

# Load data from local parquet — no Firebase call needed
df = pd.read_parquet('data/responses.parquet')
print(f'Loaded {len(df)} responses')

# Drop demographic duplicate question columns — these are copies of flat fields
demographic_duplicate_cols = ['q_101', 'q_102', 'q_103', 'q_104', 'q_105']
df = df.drop(columns=demographic_duplicate_cols, errors='ignore')

# List the 22 substantive question columns
question_cols = [f'q_{i}' for i in range(1, 23) if f'q_{i}' in df.columns]
print(f'Question columns available: {question_cols}')
print(f'Gender breakdown: {df.gender.value_counts().to_dict()}')
```

---

### Task 2: Political Orientation Overview

**Why interesting:** Core finding. Most shareable chart. Shows Bangladesh's
politically engaged youth leans left-of-centre economically but labels
itself centrist.

**Chart:** `private_analysis/charts/01_political_distribution.png`
- Horizontal bar chart
- Order: Leftist, Center Left, Centrist, Center Right,
  Rightwing, Religious Left, Religious Right
- Use LABEL_COLORS for each bar
- Show count AND percentage on each bar (e.g. "8,264  47.9%")
- Title: "Political Orientation of 17,259 Respondents"

**Table:** `private_analysis/tables/01_political_distribution.csv`
Columns: result_label, count, percentage

**Key finding to write into findings.md:**
80% lean economically left-of-centre by score, but only 9.5% call
themselves "Leftist". The word carries negative weight in Bangladesh.
This gap between score and algorithm-assigned label is the most interesting finding.

---

### Task 3: The "Centrist Illusion"

**Why interesting:** Most identity-challenging finding. People score
left but call themselves centrist. Generates high comment volume on
Facebook because it challenges self-perception.

**What to compute:**
- Among 'Centrist' labelled respondents, compute % who have
  negative economic score (economicScore < 0)
- Classify all respondents into score buckets:
  - Economically Left: economicScore < -1.5
  - Economically Centre: -1.5 to +1.5
  - Economically Right: > +1.5
- Cross-tab score bucket vs resultLabel and save to table

**Chart:** `private_analysis/charts/02_centrist_illusion.png`
- Scatter plot: economicScore (x-axis) vs socialScore (y-axis)
- All respondents as tiny light grey dots (alpha=0.15, size=8)
- 'Centrist' labelled respondents overlaid in amber (alpha=0.4, size=12)
- Draw quadrant lines at x=0 and y=0 (grey dashed)
- Annotate: what % of Centrist dots sit in x < 0 (left half)
- Title: "Where do algorithm-classified Centrists actually sit on the compass?"

**Table:** `private_analysis/tables/02_centrist_breakdown.csv`

**Facebook angle:** Post framing: "You think you are centrist.
Are you sure? Most people who scored centrist actually lean left
on economic questions." — identity-challenging posts drive comments.

---

### Task 4: The Gender Gap — Five Striking Questions

**Why interesting:** This is the most newsworthy finding for Prothom Alo.
Women differ dramatically from men on five specific questions.
Confirmed gender gaps from actual data:

```
Q16 (Equal property rights): Male=-0.23, Female=+0.59  gap=0.82
Q12 (Freedom of dress):      Male=+0.19, Female=+0.85  gap=0.67
Q9  (Laws follow religion):  Male=+0.32, Female=-0.30  gap=0.62
Q11 (Traditional norms):     Male=-0.11, Female=-0.60  gap=0.48
Q10 (Religion personal):     Male=+0.84, Female=+1.27  gap=0.43
```

**What to compute:**
- Mean response for each question split by male vs female
- Compute gap = female_mean - male_mean for all 22 questions
- Identify top 5 questions by absolute gap
- Run scipy.stats.ttest_ind on those 5 questions
- Report p-value and whether result is statistically significant (p < 0.05)

**Chart:** `private_analysis/charts/03_gender_gap_questions.png`
- Horizontal diverging bar chart
- One row per question (5 rows — top 5 by gap only)
- Male bar: navy, extends left from centre
- Female bar: amber, extends right from centre
- Zero line in the centre
- Show short question label on left side
- Add n= to legend: "Male (n=15,313)" and "Female (n=1,781)"
- Add note below: "Female sample is small (n=1,781). Interpret with caution."
- Title: "Biggest Gender Differences in Survey Responses"

**Table:** `private_analysis/tables/03_gender_gap.csv`
Columns: question_id, question_text, male_mean, female_mean, gap,
         male_classification, female_classification, p_value, significant

Note: male_classification = classify_question(male_mean, male_std_dev)
      female_classification = classify_question(female_mean, female_std_dev)
      Compute male_std_dev and female_std_dev separately before classifying.
      This lets a reader see at a glance: "men are Polarised, women Moderate
      agreement" without needing to interpret numbers.

**Key findings:**
- Q16 (equal property rights): Women strongly agree (+0.59),
  men mildly disagree (-0.23). Largest gender gap in the dataset.
- Q9 (laws follow religion): Men agree (+0.32), women disagree (-0.30).
  Direction completely reverses — not just a size difference.
- Q12 (freedom of dress): Women agree much more (+0.85 vs +0.19).

**Prothom Alo angle:** Property rights and dress freedom gaps are
concrete, relatable, and will generate reader discussion.

---

### Task 5: Most Agreed & Most Divisive Questions

**Why interesting:** Shows where this audience has consensus vs where
they split hard. Directly usable as bullet points in any press article.

**What to compute:**
- Mean response per question (q_1 to q_22)
- Standard deviation per question
- Classify each question:
  - 'Strong consensus agree' if mean > 1.0
  - 'Agreement' if mean 0.5 to 1.0
  - 'Mixed' if mean -0.5 to 0.5
  - 'Disagreement' if mean < -0.5

**Actual values from data for reference (add as comments):**
```
Highest mean:  Q17=+1.40 (env rules for factories)
               Q20=+1.15 (ban hurting religion)
               Q19=+1.14 (state supports all festivals)
Most polarised: Q9 std=1.48 (laws follow religion)
               Q16 std=1.44 (equal property rights)
               Q12 std=1.43 (freedom of dress)
Most disagreed: Q1=-0.45 (state control industries)
```

**Chart:** `private_analysis/charts/04_question_consensus.png`
- Two subplots side by side
- Left: horizontal bar of mean scores sorted high to low
  - Green if mean > 0.5, amber if -0.5 to 0.5, red if < -0.5
  - Use short question label (truncate to 8 words max)
- Right: horizontal bar of std deviation sorted high to low
  - Dark purple for high std (polarising), light purple for low
  - Label axis: "Standard deviation (higher = more divided)"
- Title: "What 17,259 Bangladeshis most agree and disagree with"

**Table:** `private_analysis/tables/04_question_analysis.csv`
Columns: question_id, question_text, category, mean, std_dev, classification
Note: classification must use classify_question(mean, std_dev) from the
Classification Logic section — NOT mean alone.

**Key findings:**
- Q17 (factory environment rules) = most agreed (+1.40).
  Near-universal support for environmental regulation.
  This crosses left/right lines — even right-leaning respondents agree.
- Q9 (laws follow religion) = most polarising (std=1.48).
  Almost no one is neutral. Two camps, very few in middle.
- Q16 (equal property rights) = second most polarising (std=1.44).
  A live social fault line in Bangladesh.

---

### Task 6: Age vs Social Questions — The Generation Gap

**Why interesting:** Counterintuitive finding.
Younger people (18-24) are MORE conservative on religious speech (Q20=+1.23)
than 35-44 group (Q20=+0.74). But 35-44 are the most secular on
religious law (Q9=-0.22). Age does not predict conservatism simply.

**What to compute:**
- Mean response for social questions:
  q_9, q_10, q_11, q_12, q_14, q_16, q_20
  grouped by age bracket
- Age order: 18-24, 25-34, 35-44, 45-54, 55+
- Include sample size (n=) for each age group

**Chart:** `private_analysis/charts/05_age_social_heatmap.png`
- Heatmap: rows = age groups, columns = social questions
- Diverging colour scale: red = positive/conservative, blue = negative/secular,
  white = zero
- Annotate each cell with mean value (1 decimal place)
- Show n= in row labels (e.g. "18-24 (n=9,234)")
- Mark 45-54 and 55+ rows with asterisk — small samples, interpret carefully
- Title: "Social Question Responses by Age Group"
- Use seaborn.heatmap with cmap='RdBu_r', center=0

**Table:** `private_analysis/tables/05_age_social.csv`

**Key findings:**
- Q20 (ban hurting religion): 18-24 most strict (+1.23),
  35-44 least strict (+0.74). Youth more sensitive about religious insult.
- Q9 (laws follow religion): 18-24 most religious (+0.38),
  35-44 most secular (-0.22). Middle-aged are most secular overall.
- Q16 (equal property rights): 35-44 most supportive (+0.12),
  18-24 least supportive (-0.18). Older group more progressive here.

---

### Task 7: Education vs Tolerance — Does Higher Education Mean More Open?

**Why interesting:** PhD holders are NOT always the most progressive.
On religious speech (Q20), SSC/HSC respondents (+1.24) agree more
strictly than PhDs (+0.61). But on minority rights (Q21), education
makes a very large difference.

**What to compute:**
- Mean response for tolerance questions:
  q_12, q_14, q_16, q_19, q_21, q_20
  grouped by education level
- Education order: below_ssc, ssc_hsc, bachelor_masters, phd

**Chart:** `private_analysis/charts/06_education_tolerance.png`
- Grouped bar chart
- X-axis: the 6 questions (short labels)
- 4 bars per question group, one per education level
- Use CAT_COLORS for 4 education levels
- Add legend with full education labels
- Title: "Responses to Tolerance Questions by Education Level"

**Table:** `private_analysis/tables/06_education_tolerance.csv`

**Key findings:**
- Q12 (freedom of dress): below_ssc=-0.19, bachelor=+0.31.
  Clear education gradient.
- Q20 (ban hurting religion): SSC/HSC agrees most strictly (+1.24),
  PhD least strictly (+0.61). Higher education reduces strictness
  on religious speech.
- Q21 (indigenous rights): below_ssc=+0.30, bachelor=+1.08.
  Strongest education effect in the dataset — education predicts
  support for minority rights more than any other question.

---

### Task 8: The Five Most Divisive Questions — Full Response Distribution

**Why interesting:** For polarising questions, showing the full
-2 to +2 distribution reveals whether it is a bimodal split
(two camps) or a normal disagreement. Bimodal = two societies.

**Questions:** Q9, Q16, Q12, Q10, Q13
(top 5 by standard deviation from actual data)

**Chart:** `private_analysis/charts/07_divisive_distributions.png`
- 5 subplots arranged 1 row x 5 columns (or 2 rows if too cramped)
- Each subplot: bar chart of response count for values -2, -1, 0, +1, +2
- Bar colours:
  -2 = '#C0392B' (dark red)
  -1 = '#E74C3C' (light red)
   0 = '#95A5A6' (grey)
  +1 = '#27AE60' (light green)
  +2 = '#1E8449' (dark green)
- X-axis labels: "Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"
- Add short question title above each subplot
- Title: "Response Distribution for the 5 Most Polarising Questions"

**Table:** `private_analysis/tables/07_divisive_distributions.csv`

**Key finding:**
Q9 (laws follow religion) and Q16 (equal property rights) show
bimodal distributions — large peaks at both extremes, shallow middle.
This means these are not questions where people are undecided.
People have strong, opposing views. That is newsworthy.

---

### Task 9: Probashi vs Bangladesh — What Living Abroad Changes

**Why interesting:** 1,270 overseas Bangladeshis participated.
Living abroad measurably shifts one question significantly:
Q20 (ban hurting religion): abroad=+0.89 vs home=+1.17.
Economic score also shifts: abroad=-0.87 vs home=-1.07.

**What to compute:**
- Mean response for all 22 questions: probashi=yes vs probashi=no
- Gap = abroad_mean - home_mean for each question
- Flag questions where abs(gap) > 0.20 as noteworthy
- Compare economicScore and socialScore means
- Run t-test for Q20 (the only clearly significant gap)

**Chart:** `private_analysis/charts/08_probashi_comparison.png`
- Lollipop / dot plot — horizontal
- One row per question (all 22)
- Two dots per row: navy = Bangladesh, green = Probashi
- Horizontal line connecting the two dots
- Longer line = bigger gap
- Sorted by gap size, largest at top
- Mark statistically significant differences with asterisk
- Title: "How Probashi Bangladeshis differ from those at home"

**Table:** `private_analysis/tables/08_probashi_comparison.csv`
Columns: question_id, question_text, home_mean, abroad_mean, gap,
         home_classification, abroad_classification, p_value

Note: apply classify_question() for home and abroad separately.

**Business Standard angle:**
Bangladesh receives $20B+ annually from the diaspora.
Probashi score slightly less left economically (-0.87 vs -1.07)
and are less strict on religious speech. Exposure to market
economies and diverse societies measurably shifts views.
That is a data-driven angle for a diaspora policy story.

---

### Task 10: Occupation — Businesspeople vs Everyone Else

**Why interesting:** Businesspeople are the only occupational group
that leans meaningfully right economically (economic score -0.34).
Everyone else: students=-1.09, service=-1.11, homemakers=-1.03.
Businesspeople also most strongly support property rights (Q8).

**What to compute:**
- Mean economicScore and socialScore by occupation
- Mean response on Q1, Q3, Q7, Q8 (four most economically revealing
  questions) grouped by occupation
- These four show the sharpest occupation-based differences

**Chart:** `private_analysis/charts/09_occupation_economics.png`
- Two subplots:
- Left: horizontal bar of mean economicScore by occupation
  — sorted from most left to most right
  — colour each bar: navy for left-leaning, amber for right-leaning
- Right: grouped bar for Q3 (tax rich), Q7 (free healthcare),
  Q8 (property rights) across occupation groups
  — use CAT_COLORS for occupation groups
- Title: "Economic Views by Occupation"

**Table:** `private_analysis/tables/09_occupation_scores.csv`

**Key finding:**
Businesspeople are the predictable exception — they resist taxing
the rich and value property rights most. Students and service
workers want free healthcare most strongly.
Economic self-interest shapes economic opinions — this is coherent
and worth a paragraph in a Business Standard article.

---

### Task 11: Growth Over Time — The Viral Story

**Why interesting:** Zero paid advertising at launch.
17,259 organic responses in 14 days from Facebook alone.
This is the meta-story about the project itself.

**What to compute:**
- Parse createdAt to datetime
  (format example: "2026-04-03T15:21:16.728Z" — use pd.to_datetime with utc=True)
- Count responses per calendar day
- Identify peak day (date with most responses)
- Compute cumulative total
- Compute average responses per day

**Chart:** `private_analysis/charts/10_growth_over_time.png`
- Two subplots stacked vertically (2 rows, 1 column)
- Top: bar chart of daily response count
  — bars coloured navy
  — peak day bar coloured amber with annotation "Peak: {n} responses"
- Bottom: line chart of cumulative total
  — navy line with filled area underneath (alpha=0.2)
  — annotate final point with total
- X-axis: dates Apr 3 to Apr 17 (format: "Apr 3", "Apr 4" etc.)
- Title: "How 17,259 Bangladeshis discovered Bam-Dan in 14 days"

**Table:** `private_analysis/tables/10_daily_growth.csv`
Columns: date, daily_count, cumulative_total

**Business Standard tech angle:**
Built with Firebase and React. Zero ad spend at launch.
17K responses in 14 days. One of Bangladesh's most successful
civic tech tools of 2026. The growth curve itself is a story
about the appetite for political self-reflection tools in South Asia.

---

### Task 12: Auto-generate findings.md

Final cell — write `private_analysis/findings.md` dynamically.
Every number must come from computed variables, not hardcoded.

```markdown
# Bam-Dan Survey Key Findings
Generated: {today}
Sample: {total_count} responses | April 3-17 2026 | bam-dan.com

## IMPORTANT: Sample Caveat
Self-selected online sample. {male_pct:.1f}% male, {student_pct:.1f}% students.
These findings describe Bangladesh's politically engaged online youth,
not the general population.

## 1. The Centrist Illusion
{pct_centrists_scoring_left:.1f}% of algorithm-classified Centrists have a
negative (left-of-centre) economic score.

## 2. Biggest Gender Gap
Q16 (Equal property rights for men and women):
  Male mean = {q16_male:.2f}, Female mean = {q16_female:.2f}
  Gap = {q16_gap:.2f} — largest gender difference in the dataset.

## 3. Most Agreed Question
Q{top_q_id} - "{top_q_text}"
  Mean response: {top_q_mean:.2f} (near-universal agreement)

## 4. Most Divisive Question
Q{divisive_q_id} - "{divisive_q_text}"
  Standard deviation: {divisive_q_std:.2f} — bimodal distribution,
  two strong opposing camps.

## 5. Generation Surprise
Q20 (Strictly ban anything hurting religious sentiments):
  18-24 age group mean = {q20_young:.2f}
  35-44 age group mean = {q20_mid:.2f}
  Younger respondents are stricter on religious speech.

## 6. Education and Minority Rights
Q21 (Special rights for indigenous/ethnic minorities):
  Below SSC mean = {q21_low_edu:.2f}
  Bachelor/Masters mean = {q21_high_edu:.2f}
  Education is the strongest predictor of support for minority rights.

## 7. Probashi Difference
Q20 (Strictly ban anything hurting religious sentiments):
  Bangladesh respondents mean = {q20_home:.2f}
  Probashi (abroad) mean = {q20_abroad:.2f}
  Difference = {q20_diff:.2f}

## 8. Growth Story
Peak day: {peak_date} ({peak_count} responses in one day)
Total responses: {total_count} over {total_days} days
Average per day: {avg_per_day:.0f}
```

---

## Summary: Which Tasks Map to Which Outlet

| Task | Output file | Best for |
|------|-------------|----------|
| 2 — Political distribution | 01_political_distribution | All three outlets |
| 3 — Centrist illusion | 02_centrist_illusion | Daily Star, Facebook |
| 4 — Gender gap | 03_gender_gap_questions | Prothom Alo |
| 5 — Consensus & divisive | 04_question_consensus | All three outlets |
| 6 — Age vs social | 05_age_social_heatmap | Daily Star |
| 7 — Education tolerance | 06_education_tolerance | Prothom Alo, Daily Star |
| 8 — Divisive distributions | 07_divisive_distributions | Daily Star |
| 9 — Probashi | 08_probashi_comparison | Business Standard |
| 10 — Occupation economics | 09_occupation_economics | Business Standard |
| 11 — Growth story | 10_growth_over_time | Business Standard |
