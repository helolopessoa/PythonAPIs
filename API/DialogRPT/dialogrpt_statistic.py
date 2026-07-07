import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# carregar dados
df = pd.read_csv("dialogrpt_full_results.csv")

# separar grupos
baseline = df[df["condition"] == "baseline"]
scaffolded = df[df["condition"] == "scaffold"]

# ------------------------
# MÉDIA E DESVIO PADRÃO
# ------------------------

print("\n=== MÉDIAS ===")
print(df.groupby(["mode","condition"])["dialogrpt"].mean())

print("\n=== DESVIO PADRÃO ===")
print(df.groupby(["mode","condition"])["dialogrpt"].std())

# ------------------------
# T-TEST + COHEN'S D
# ------------------------

def cohens_d(group1, group2):
    mean_diff = np.mean(group2) - np.mean(group1)
    pooled_sd = np.sqrt((np.var(group1) + np.var(group2)) / 2)
    return mean_diff / pooled_sd if pooled_sd != 0 else 0


print("\n=== TESTES ===")

for mode in df["mode"].unique():
    print(f"\n--- MODE: {mode.upper()} ---")

    base = df[(df["mode"] == mode) & (df["condition"] == "baseline")]["dialogrpt"]
    scaff = df[(df["mode"] == mode) & (df["condition"] == "scaffold")]["dialogrpt"]

    t, p = ttest_ind(base, scaff, equal_var=False)
    d = cohens_d(base, scaff)

    print(f"Baseline mean: {base.mean():.4f}")
    print(f"Scaffolded mean: {scaff.mean():.4f}")
    print(f"p-value: {p:.4f}")
    print(f"Cohen's d: {d:.4f}")