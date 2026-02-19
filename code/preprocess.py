# preprocess.py
# ECON 570 – eBay Replication
# Creates pivot tables and reproduces Figures 5.2 and 5.3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Step 1 — Load and prepare data
# -----------------------------
df = pd.read_csv('input/PaidSearch.csv')

df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# -----------------------------
# Step 2 — Create pivot tables
# -----------------------------

# Separate groups
treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

def create_pivot(data, filename):
    pivot = data.pivot_table(
        index='dma',
        columns='treatment_period',
        values='log_revenue',
        aggfunc='mean'
    )

    # Rename columns
    pivot = pivot.rename(columns={
        0: 'log_revenue_pre',
        1: 'log_revenue_post'
    })

    # Compute difference
    pivot['log_revenue_diff'] = (
        pivot['log_revenue_post'] - pivot['log_revenue_pre']
    )

    # Save
    pivot.to_csv(filename)

# Save pivot tables
create_pivot(treated, 'temp/treated_pivot.csv')
create_pivot(untreated, 'temp/untreated_pivot.csv')

# -----------------------------
# Step 3 — Print summary stats
# -----------------------------
print("Treated DMAs:", treated['dma'].nunique())
print("Untreated DMAs:", untreated['dma'].nunique())
print("Date range:", df['date'].min().date(), "to", df['date'].max().date())

# -----------------------------
# Step 4 — Reproduce Figure 5.2
# -----------------------------
daily_rev = (
    df.groupby(['date', 'search_stays_on'])['revenue']
      .mean()
      .reset_index()
)

plt.figure(figsize=(10,6))

# Control group
control = daily_rev[daily_rev['search_stays_on'] == 1]
plt.plot(control['date'], control['revenue'],
         label='Control (search stays on)')

# Treatment group
treat = daily_rev[daily_rev['search_stays_on'] == 0]
plt.plot(treat['date'], treat['revenue'],
         label='Treatment (search goes off)')

# Treatment date line
plt.axvline(pd.Timestamp('2012-05-22'),
            linestyle='--')

plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Average Revenue Over Time')
plt.legend()

plt.tight_layout()
plt.savefig('output/figures/figure_5_2.png')
plt.close()

# -----------------------------
# Step 5 — Reproduce Figure 5.3
# -----------------------------
daily_log = (
    df.groupby(['date', 'search_stays_on'])['log_revenue']
      .mean()
      .reset_index()
)

pivot_log = daily_log.pivot(
    index='date',
    columns='search_stays_on',
    values='log_revenue'
)

# Difference: control - treatment
pivot_log['diff'] = pivot_log[1] - pivot_log[0]

plt.figure(figsize=(10,6))
plt.plot(pivot_log.index, pivot_log['diff'])

plt.axvline(pd.Timestamp('2012-05-22'),
            linestyle='--')

plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log Revenue Difference Over Time')

plt.tight_layout()
plt.savefig('output/figures/figure_5_3.png')
plt.close()

