"""
Week 6 Task: Comprehensive Evaluation and Reporting on Digital
Transformation Insights
----------------------------------------------------------------
This script does not introduce new analysis; it re-runs the full
Week 2 -> Week 5 pipeline end-to-end and prints a consolidated
summary of every key statistic used across the final report,
so the entire project can be reproduced and verified in one go.
"""

import subprocess
import sys

STEPS = [
    ("Week 2 - Data Collection & Cleaning", "week2_data_collection_cleaning.py"),
    ("Week 3 - Exploratory Data Analysis", "week3_eda_visualization.py"),
    ("Week 4 - Statistical Analysis", "week4_statistical_analysis.py"),
    ("Week 5 - Predictive Modeling", "week5_predictive_modeling.py"),
]


def run_pipeline():
    for title, script in STEPS:
        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)
        subprocess.run([sys.executable, script], check=True)


def print_final_summary():
    print("\n" + "#" * 70)
    print("FINAL SUMMARY - KEY RESULTS ACROSS ALL WEEKS")
    print("#" * 70)
    print("""
Week 2 : Merged dataset -> 36 states/UTs, 8 columns, 0 missing values.

Week 3 : 4 visualizations generated (top-10 adoption, rural/urban CSC
         split, adoption-infrastructure correlation, GP coverage rate).

Week 4 : Pearson r (CSC Total vs DigiLocker) = 0.835, p < 0.001
         Pearson r (GP Coverage vs DigiLocker) = 0.418, p = 0.014
         Linear Regression R^2 = 0.697, p < 0.001
         Welch's t-test (High vs Low GP coverage): t = 3.24, p = 0.004

Week 5 : Predictors: Functional_CSC_Total + GP_Coverage_Ratio
         Train R^2 = 0.706 | Test R^2 = 0.585
         Test MAE  = 21,19,785 | Test RMSE = 22,95,877
         Gujarat +20% CSC scenario -> demand +14.01%

Week 6 : Recommendation - prioritize CSC expansion + GP-level equity
         tracking, supported by additional digital-readiness data
         (literacy, internet penetration) in future iterations.
""")


if __name__ == "__main__":
    run_pipeline()
    print_final_summary()
