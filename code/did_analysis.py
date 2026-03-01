# DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex

import pandas as pd
import numpy as np
import os

# Load pivot tables
treated = pd.read_csv("temp/treated_pivot.csv", index_col=0)
untreated = pd.read_csv("temp/untreated_pivot.csv", index_col=0)

# Compute log revenue
treated_log = np.log(treated)
untreated_log = np.log(untreated)

# Compute pre-post change for each DMA
treated_diff = treated_log.iloc[-1] - treated_log.iloc[0]
untreated_diff = untreated_log.iloc[-1] - untreated_log.iloc[0]

# Means
r1 = treated_diff.mean()
r0 = untreated_diff.mean()

# DID estimate
gamma_hat = r1 - r0

# Standard error
se = np.sqrt(treated_diff.var(ddof=1)/len(treated_diff) +
             untreated_diff.var(ddof=1)/len(untreated_diff))

# 95% confidence interval
ci_low = gamma_hat - 1.96*se
ci_high = gamma_hat + 1.96*se

print("Gamma hat:", round(gamma_hat, 4))
print("Std Error:", round(se, 4))
print("95% CI:", [round(ci_low,4), round(ci_high,4)])

# Save LaTeX table
os.makedirs("output/tables", exist_ok=True)

with open("output/tables/did_table.tex", "w") as f:
    f.write("\\begin{tabular}{lccc}\n")
    f.write("\\hline\n")
    f.write("Estimate & Std. Error & CI Low & CI High \\\\\n")
    f.write("\\hline\n")
    f.write(f"{gamma_hat:.4f} & {se:.4f} & {ci_low:.4f} & {ci_high:.4f} \\\\\n")
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
