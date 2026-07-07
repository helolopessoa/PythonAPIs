import pandas as pd 
from scipy import stats
import numpy as np

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("results_full.csv")
# df = pd.read_csv("results_test_final - results_test_final.csv")

print("\n📊 TOTAL ROWS:", len(df))

# =========================
# PADRONIZAÇÃO
# =========================

df["condition"] = df["condition"].str.lower().str.strip()
df["culture"] = df["culture"].str.strip()
df["trait"] = df["trait"].str.strip()

# =========================
# FIX NUMERIC COLUMNS
# =========================

numeric_cols = ["rating", "rating_norm", "alignment", "alignment_norm"]

for col in numeric_cols:
    df[col] = df[col].astype(str).str.strip()  # limpa espaços
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 🔥 IMPORTANTE (novo)
df["inferred_rating"] = df["inferred_rating"].astype(str).str.upper().str.strip()

print("\nDTYPES:")
print(df.dtypes)

# =========================
# SPLITS: INFERRED VS NOT
# =========================

df_all = df.copy()
df_inferred = df[df["inferred_rating"] == "TRUE"]
df_not_inferred = df[df["inferred_rating"] == "FALSE"]

splits = {
    "ALL": df_all,
    "INFERRED_ONLY": df_inferred,
    "NOT_INFERRED": df_not_inferred
}

# =========================
# FUNÇÕES
# =========================

def cohens_d(a, b):
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled_std = np.sqrt(
        ((np.std(a, ddof=1) ** 2) + (np.std(b, ddof=1) ** 2)) / 2
    )
    if pooled_std == 0:
        return 0
    return (np.mean(a) - np.mean(b)) / pooled_std


def analyze_subset(data, label, metric):
    print(f"\n=========================")
    print(f"{label} | {metric.upper()}")
    print(f"=========================")

    if metric not in data.columns:
        print(f"⚠ Metric '{metric}' not found")
        return

    if "condition" not in data.columns:
        print("⚠ No condition column — descriptive stats only")
        print("Mean:", round(data[metric].mean(), 4))
        print("Std:", round(data[metric].std(), 4))
        return

    baseline = data[data["condition"] == "baseline"][metric].dropna()
    scaffold = data[data["condition"] == "scaffold"][metric].dropna()

    print(f"n_baseline={len(baseline)} | n_scaffold={len(scaffold)}")

    if len(baseline) < 2 or len(scaffold) < 2:
        print("⚠ Not enough data for statistical test")
        return

    mean_b, std_b = baseline.mean(), baseline.std()
    mean_s, std_s = scaffold.mean(), scaffold.std()

    print(f"Baseline: {mean_b:.4f} (± {std_b:.4f})")
    print(f"Scaffold: {mean_s:.4f} (± {std_s:.4f})")

    t_stat, p_value = stats.ttest_ind(scaffold, baseline, equal_var=False)

    print(f"\nP-value: {p_value:.6f}")
    print("👉 Significant" if p_value < 0.05 else "👉 Not significant")

    d = cohens_d(scaffold, baseline)
    print(f"Cohen's d: {d:.4f}")


# =========================
# EXTRA ANALYSIS: INFERRED + ALIGNMENT RATES
# =========================

print("\n\n#########################################")
print("📊 INFERRED RATE")
print("#########################################")

for culture in df["culture"].unique():
    for condition in ["baseline", "scaffold"]:
        subset = df[(df["culture"] == culture) & (df["condition"] == condition)]

        total = len(subset)
        inferred = len(subset[subset["inferred_rating"] == "TRUE"])

        perc = (inferred / total) * 100 if total > 0 else 0

        print(f"{culture} | {condition} → {perc:.2f}% inferred (n={inferred}/{total})")


print("\n\n#########################################")
print("🌍 CULTURAL ALIGNMENT RATE")
print("#########################################")

for culture in df["culture"].unique():
    for condition in ["baseline", "scaffold"]:
        subset = df[(df["culture"] == culture) & (df["condition"] == condition)]

        mean_align = subset["alignment_norm"].mean()

        print(f"{culture} | {condition} → {mean_align*100:.2f}% alignment")


print("\n\n#########################################")
print("📉 ALIGNMENT DIFFERENCE (Scaffold - Baseline)")
print("#########################################")

for culture in df["culture"].unique():
    base = df[(df["culture"] == culture) & (df["condition"] == "baseline")]["alignment_norm"].mean()
    scaf = df[(df["culture"] == culture) & (df["condition"] == "scaffold")]["alignment_norm"].mean()

    diff = scaf - base

    print(f"{culture} → Δ = {diff:.4f}")



# =========================
# LOOP PRINCIPAL POR SPLIT
# =========================

for split_name, split_df in splits.items():

    print("\n\n#########################################")
    print(f"📦 DATA SPLIT: {split_name}")
    print("#########################################")

    # =========================
    # POR CULTURA
    # =========================

    for culture in split_df["culture"].unique():

        print("\n#################################")
        print(f"🌍 CULTURE: {culture}")
        print("#################################")

        subset = split_df[split_df["culture"] == culture]

        analyze_subset(subset, culture, "alignment_norm")
        analyze_subset(subset, culture, "rating_norm")

    # =========================
    # POR TRAÇO DENTRO DE CULTURA
    # =========================

    print("\n\n=========================")
    print("🧠 BY TRAIT (PER CULTURE)")
    print("=========================")

    for culture in split_df["culture"].unique():

        print(f"\n=== {culture} ===")

        subset_culture = split_df[split_df["culture"] == culture]

        for trait in subset_culture["trait"].unique():

            subset = subset_culture[subset_culture["trait"] == trait]

            baseline = subset[subset["condition"] == "baseline"]["alignment_norm"].dropna()
            scaffold = subset[subset["condition"] == "scaffold"]["alignment_norm"].dropna()

            print(f"\n{trait} → n_b={len(baseline)}, n_s={len(scaffold)}")

            if len(baseline) < 2 or len(scaffold) < 2:
                print("⚠ Not enough data")
                continue

            t_stat, p_value = stats.ttest_ind(scaffold, baseline, equal_var=False)
            d = cohens_d(scaffold, baseline)

            print(f"{trait}: p={p_value:.5f} | d={d:.3f}")            

# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()

# for condition in ["baseline", "scaffold"]:
#     subset = df[df["condition"] == condition]
#     means = subset.groupby("culture")["rating_norm"].mean()
    
#     ax.bar(
#         [x + (0 if condition == "baseline" else 0.4) for x in range(len(means))],
#         means.values,
#         width=0.4,
#         label=condition
#     )

# ax.set_xticks([0.2, 1.2])
# ax.set_xticklabels(means.index)
# ax.set_ylabel("Rating (normalized)")
# ax.set_title("Rating by Culture and Condition")
# ax.legend()

# plt.show()

import matplotlib.pyplot as plt
import numpy as np

cultures = ["Ranger", "Downside"]

baseline = [67.21, 52.29]
scaffold = [66.99, 43.64]

x = np.arange(len(cultures))
width = 0.35

fig, ax = plt.subplots()

ax.bar(x - width/2, baseline, width, label="Baseline")
ax.bar(x + width/2, scaffold, width, label="Scaffold")

ax.set_ylabel("Alignment (%)")
ax.set_title("Cultural Alignment (Non-Inferred Responses)")
ax.set_xticks(x)
ax.set_xticklabels(cultures)
ax.legend()

plt.show()