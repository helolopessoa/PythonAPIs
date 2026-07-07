
from usr_data_treatment import load_dataset
from usr_metrics import USRScorer, summarize_results
from scipy.stats import ttest_ind
import numpy as np
import csv


# carregar dados
baseline = load_dataset("../DataUSR/Baseline")
scaffold = load_dataset("../DataUSR/Scaffold")

# inicializar USR
usr = USRScorer()

# calcular
baseline_scores = usr.score_dataset(baseline)
scaffold_scores = usr.score_dataset(scaffold)

# resumir
baseline_summary = summarize_results(baseline_scores)
scaffold_summary = summarize_results(scaffold_scores)

print("Baseline:", baseline_summary)
print("Scaffold:", scaffold_summary)

baseline_means = [d["mean"] for d in baseline_scores]
scaffold_means = [d["mean"] for d in scaffold_scores]

t_stat, p_value = ttest_ind(baseline_means, scaffold_means)

print("t-stat:", t_stat)
print("p-value:", p_value)

mean_diff = np.mean(scaffold_means) - np.mean(baseline_means)

pooled_std = np.sqrt(
    (np.std(baseline_means) ** 2 + np.std(scaffold_means) ** 2) / 2
)

cohen_d = mean_diff / pooled_std

print("Cohen's d:", cohen_d)


def export_to_csv(results, condition, output_file):
    """
    Exporta resultados de diálogos para CSV
    """
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # escreve header só se arquivo estiver vazio
        if f.tell() == 0:
            writer.writerow(["file", "condition", "mean", "std", "min", "max", "n_turns"])

        for r in results:
            writer.writerow([
                r["file"],
                condition,
                r["mean"],
                r["std"],
                r["min"],
                r["max"],
                r["n_turns"]
            ])

# depois de calcular os scores
export_to_csv(baseline_scores, "baseline", "usr_results.csv")
export_to_csv(scaffold_scores, "scaffold", "usr_results.csv")