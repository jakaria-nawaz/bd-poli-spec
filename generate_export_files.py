import os
import pandas as pd

os.makedirs("private_analysis", exist_ok=True)

df = pd.read_parquet("data/responses.parquet")

# Sort q_1..q_22 columns numerically
q_cols = sorted([c for c in df.columns if c.startswith("q_") and c[2:].isdigit() and 1 <= int(c[2:]) <= 22],
                key=lambda x: int(x[2:]))

base_cols = ["age", "gender", "education", "occupation", "probashi",
             "createdAt", "meta_platform", "meta_language"]

# Set 1: no scores / resultLabel
set1_cols = base_cols + q_cols
df_set1 = df[set1_cols]

# Set 2: with scores / resultLabel
set2_cols = base_cols + q_cols + ["economicScore", "socialScore", "resultLabel"]
df_set2 = df[set2_cols]

df_set1.to_csv("private_analysis/survey_anonymised.csv", index=False)
df_set1.to_parquet("private_analysis/survey_anonymised.parquet", index=False)

df_set2.to_csv("private_analysis/survey_with_scores.csv", index=False)
df_set2.to_parquet("private_analysis/survey_with_scores.parquet", index=False)

print("Set 1:", df_set1.shape, list(df_set1.columns))
print("Set 2:", df_set2.shape, list(df_set2.columns))
print("Done.")
