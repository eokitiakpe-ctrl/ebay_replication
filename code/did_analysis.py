# did_analysis.py — Person B revision
# Computes DID estimate for the eBay paid search shutdown experiment.
# Approach: Compare log revenue changes pre vs post across treatment/control DMAs.
# Data source: pivot tables generated in preprocess.py.
# Output file: output/tables/did_table.tex (LaTeX formatted).
# Includes additional robustness documentation.

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


# Exponentiated (levels) results
gamma_hat_exp = np.exp(gamma_hat)
ci_lower_exp = np.exp(ci_low)
ci_upper_exp = np.exp(ci_high)


# Save LaTeX table
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lcc}
\hline
 & Log Scale & Levels (exp) \\
\hline
Point Estimate ($\hat{\gamma}$) & %.4f & %.4f \\
Standard Error & %.4f & --- \\
95\%% CI & [%.4f, %.4f] & [%.4f, %.4f] \\
\hline
\end{tabular}
\label{tab:did}
\end{table}
""" % (
    gamma_hat,
    gamma_hat_exp,
    se,
    ci_low,
    ci_high,
    ci_lower_exp,
    ci_upper_exp
)

with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)
