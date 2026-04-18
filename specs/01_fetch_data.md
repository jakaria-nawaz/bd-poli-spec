# Spec: Fetch Firestore Data to Local Parquet

## Goal
Fetch all documents from the Firestore `results` and `metadata` collections
and save them as local files inside `data/` for offline analysis.

## Context
- Firebase project is already set up
- `serviceAccountKey.json` exists in project root (never committed)
- Collection name for responses: `results`
- Collection name for question/methodology config: `metadata`
- ~17,000 documents expected in `results`

## Development Environment
- All work must be done inside a Python virtual environment
- Virtual environment folder name: `venv`
- Add `venv/` to `.gitignore`
- Setup instructions:
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

## Code Style & Readability
- Written for junior developers — clarity over cleverness
- Every non-obvious line must have a short comment explaining why
- Use descriptive variable names (e.g. `all_documents` not `docs`)
- Avoid one-liners — split into readable steps
- No classes, no decorators, no abstractions
- Each function does exactly one thing

## Document Structure (one result document)

Flat fields:
- `createdAt` (string, ISO timestamp)
- `district` (string or null — 100% null in practice, skip geographic analysis)
- `economicScore` (number)
- `socialScore` (number)
- `resultLabel` (string, e.g. "Centrist")
- `gender` (string)
- `education` (string)
- `occupation` (string)
- `probashi` (string, "yes"/"no")
- `age` (string)
- `emailOrFacebook` (string — PII, present in raw data, excluded from all exports)
- `consentAccepted` (bool — not analytically useful, excluded from exports)

Nested object — `metadata`:
- `language` (string) → flattened to `meta_language`
- `platform` (string) → flattened to `meta_platform`
- `userAgent` (string) → flattened to `meta_userAgent` (PII-adjacent, excluded from exports)
- `ip` (string) → flattened to `meta_ip` (PII, excluded from exports)
- `isp` (string) → flattened to `meta_isp` (excluded from exports)
- `city` (string) → flattened to `meta_city` (excluded from exports)
- `region` (string) → flattened to `meta_region` (excluded from exports)
- `country` (string) → flattened to `meta_country` (excluded from exports)

Nested map — `rawAnswers`:
- Keys are question IDs (integers or strings)
- Values are integers (-2 to +2)
- Example: `{1: -1, 2: 2, 3: 1, ...}`
- Flattened to `q_1`, `q_2`, ... `q_22` (substantive questions)
- Also includes `q_101` through `q_105` (demographic duplicate questions — excluded from analysis)

## Tasks

### Task 1: Create `requirements.txt`
```
firebase-admin
pandas
pyarrow
jupyter
matplotlib
seaborn
scipy
```

### Task 2: Create `.gitignore`
```
# Environment
venv/
__pycache__/
*.pyc
.env

# Credentials — never commit
serviceAccountKey.json

# Raw data — contains unverified PII fields; fetched locally via fetch_data.py
data/

# Private analysis outputs — charts, tables, full exports
private_analysis/

# IDE
.vscode/
.idea/

# macOS
.DS_Store

# Jupyter
.ipynb_checkpoints/
```

### Task 3: Create `fetch_data.py`

- Create the `data/` folder if it does not exist before any saves
- Initialize Firebase using `serviceAccountKey.json`
- Stream all documents from `results` collection
- For each result document:
  - Copy all flat fields directly
  - Flatten `metadata` nested object → prefix each key with `meta_` (e.g. `meta_language`)
  - Flatten `rawAnswers` nested map → prefix each key with `q_` (e.g. `q_1`, `q_2`)
  - Add `doc_id` from `document_snapshot.id`
  - Skip original nested keys `metadata` and `rawAnswers`
- Build a pandas DataFrame from all result rows
- Print row count and column list
- Save to `data/responses.parquet`
- Stream all documents from `metadata` collection (flat structure)
- Save raw metadata to `data/metadata.json` (UTF-8, human-readable indent)
- Save metadata to `data/metadata.parquet`
- Extract the `questions_v1` document from metadata and save its `questions` list
  to `data/questions_v1.parquet`
- Print confirmation after each save

### Task 4: Create `analysis.ipynb`
A Jupyter notebook with quick sanity checks — used to verify a fresh fetch is correct.
Reads from `data/responses.parquet` (not project root).

Cell 1 — Imports:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

Cell 2 — Load data:
```python
df = pd.read_parquet("data/responses.parquet")
print(f"{len(df)} responses loaded")
print(df.dtypes)
```

Cell 3 — Sanity checks:
```python
print(df["economicScore"].describe())
print(df["socialScore"].describe())
print(df["resultLabel"].value_counts())
print(df["gender"].value_counts())
print(df["occupation"].value_counts())
print(df["education"].value_counts())
```

Cell 4 — Score distribution chart:
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df["economicScore"].hist(bins=30, ax=axes[0], color="steelblue")
axes[0].set_title("Economic Score Distribution")
df["socialScore"].hist(bins=30, ax=axes[1], color="coral")
axes[1].set_title("Social Score Distribution")
plt.tight_layout()
plt.show()
```

Cell 5 — Cross-tab:
```python
pd.crosstab(df["occupation"], df["resultLabel"])
```

## Constraints
- Do NOT modify `serviceAccountKey.json`
- Do NOT hardcode any credentials in any file
- Keep all code simple and readable — no classes, no abstractions
- `fetch_data.py` should be runnable as a plain Python script: `python fetch_data.py`
- All raw data files go in `data/` — never in the project root
- `data/` is gitignored — never commit raw survey data
- Spec files live in `specs/`
