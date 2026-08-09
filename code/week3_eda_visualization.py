"""
Week 3 Task: Exploratory Data Analysis and Visualization
----------------------------------------------------------------
Generates descriptive statistics and 4 visualizations from the
merged dataset produced in Week 2.

Requires: data/merged_data.csv (run week2_data_collection_cleaning.py first)
Outputs: charts/chart1_top10_digilocker.png
         charts/chart2_csc_rural_urban.png
         charts/chart3_correlation.png
         charts/chart4_gp_coverage.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DATA_PATH = "data/merged_data.csv"
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Functional_Ratio_pct"] = (
        df["GPs_with_Functional_CSC"] / df["No_of_GPs"] * 100
    ).round(2)
    return df


def descriptive_stats(df):
    print("=== Descriptive Statistics ===")
    print(df[["DigiLocker_Users", "Functional_CSC_Total", "Functional_Ratio_pct"]].describe())


def chart1_top10_digilocker(df):
    top10 = df.sort_values("DigiLocker_Users", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(top10["State"][::-1], top10["DigiLocker_Users"][::-1] / 1e6, color="#E8730A")
    ax.set_xlabel("Registered Users (in Millions)")
    ax.set_title("Top 10 States/UTs by DigiLocker Registered Users", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1fM"))
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.3, bar.get_y() + bar.get_height() / 2, f"{w:.1f}M", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/chart1_top10_digilocker.png", dpi=150)
    plt.close()


def chart2_csc_rural_urban(df):
    top10 = df.sort_values("Functional_CSC_Total", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = range(len(top10))
    ax.bar(x, top10["Functional_CSC_Rural"], label="Rural CSCs", color="#2E7D32")
    ax.bar(x, top10["Functional_CSC_Urban"], bottom=top10["Functional_CSC_Rural"],
           label="Urban CSCs", color="#F9A825")
    ax.set_xticks(list(x))
    ax.set_xticklabels(top10["State"], rotation=40, ha="right", fontsize=9)
    ax.set_ylabel("Number of Functional CSCs")
    ax.set_title("Top 10 States by Functional CSCs (Rural vs Urban Split)", fontsize=13, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/chart2_csc_rural_urban.png", dpi=150)
    plt.close()


def chart3_correlation(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["Functional_CSC_Total"], df["DigiLocker_Users"] / 1e6,
               color="#1565C0", s=50, alpha=0.7, edgecolor="black")
    m, b = np.polyfit(df["Functional_CSC_Total"], df["DigiLocker_Users"] / 1e6, 1)
    r = df["Functional_CSC_Total"].corr(df["DigiLocker_Users"])
    xs = np.linspace(df["Functional_CSC_Total"].min(), df["Functional_CSC_Total"].max(), 100)
    ax.plot(xs, m * xs + b, color="red", linestyle="--", label=f"Trend line (r={r:.2f})")
    ax.set_xlabel("Functional CSCs (Total)")
    ax.set_ylabel("DigiLocker Registered Users (Millions)")
    ax.set_title("Correlation: Digital Service Infrastructure vs Adoption", fontsize=12, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/chart3_correlation.png", dpi=150)
    plt.close()


def chart4_gp_coverage(df):
    top10 = df.sort_values("Functional_Ratio_pct", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(top10["State"], top10["Functional_Ratio_pct"], color="#6A1B9A")
    ax.set_ylabel("% of Gram Panchayats with Functional CSC")
    ax.set_title("Top 10 States: Gram Panchayat CSC Coverage Rate", fontsize=13, fontweight="bold")
    ax.set_xticks(range(len(top10)))
    ax.set_xticklabels(top10["State"], rotation=40, ha="right", fontsize=9)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.0f}%", ha="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/chart4_gp_coverage.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    data = load_data()
    descriptive_stats(data)
    chart1_top10_digilocker(data)
    chart2_csc_rural_urban(data)
    chart3_correlation(data)
    chart4_gp_coverage(data)
    print(f"\n4 charts saved in '{CHART_DIR}/'")
