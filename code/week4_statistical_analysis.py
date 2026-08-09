"""
Week 4 Task: Statistical Analysis of E-Governance Performance Metrics
----------------------------------------------------------------------
Applies Pearson correlation, linear regression, and a Welch's t-test
on the merged dataset to formally test the relationships explored
visually in Week 3.

Requires: data/merged_data.csv
"""

import pandas as pd
from scipy import stats

DATA_PATH = "data/merged_data.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Functional_Ratio_pct"] = df["GPs_with_Functional_CSC"] / df["No_of_GPs"] * 100
    return df


def correlation_analysis(df):
    print("=== 1. Pearson Correlation Analysis ===")
    r1, p1 = stats.pearsonr(df["Functional_CSC_Total"], df["DigiLocker_Users"])
    print(f"CSC Total vs DigiLocker Users:      r = {r1:.4f}, p = {p1:.6f}  (n={len(df)})")

    sub = df.dropna(subset=["Functional_Ratio_pct"])
    r2, p2 = stats.pearsonr(sub["Functional_Ratio_pct"], sub["DigiLocker_Users"])
    print(f"GP Coverage Ratio vs DigiLocker:    r = {r2:.4f}, p = {p2:.6f}  (n={len(sub)})")
    print()


def regression_analysis(df):
    print("=== 2. Simple Linear Regression ===")
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df["Functional_CSC_Total"], df["DigiLocker_Users"]
    )
    print(f"DigiLocker_Users = {slope:.4f} * Functional_CSC_Total + {intercept:.2f}")
    print(f"R-squared = {r_value ** 2:.4f}, p = {p_value:.6f}, std_err = {std_err:.4f}")
    print()


def hypothesis_test(df):
    print("=== 3. Hypothesis Testing (Welch's t-test) ===")
    median_ratio = df["Functional_Ratio_pct"].median()
    high = df[df["Functional_Ratio_pct"] >= median_ratio]["DigiLocker_Users"]
    low = df[df["Functional_Ratio_pct"] < median_ratio]["DigiLocker_Users"]

    print(f"Median GP coverage ratio: {median_ratio:.2f}%")
    print(f"High-coverage group: n={len(high)}, mean={high.mean():,.0f}")
    print(f"Low-coverage group:  n={len(low)}, mean={low.mean():,.0f}")

    t_stat, t_p = stats.ttest_ind(high, low, equal_var=False)
    print(f"Welch t-test: t = {t_stat:.4f}, p = {t_p:.4f}")
    print()


if __name__ == "__main__":
    data = load_data()
    correlation_analysis(data)
    regression_analysis(data)
    hypothesis_test(data)
