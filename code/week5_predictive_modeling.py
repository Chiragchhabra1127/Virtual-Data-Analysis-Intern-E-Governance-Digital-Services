"""
Week 5 Task: Predictive Modeling for Digital Service Demand Forecasting
--------------------------------------------------------------------------
Trains and evaluates a multiple linear regression model to forecast
DigiLocker adoption from CSC infrastructure metrics.

Predictors used (final, updated version):
    - Functional_CSC_Total
    - Functional_Ratio_pct  (GP coverage ratio)
Note: Rural/Urban CSC split was deliberately excluded as a separate
predictor since it is a component of the Total and caused multicollinearity.

Requires: data/merged_data.csv
Outputs:  charts/chart6_actual_vs_predicted.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = "data/merged_data.csv"
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

FEATURES = ["Functional_CSC_Total", "Functional_Ratio_pct"]
TARGET = "DigiLocker_Users"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Functional_Ratio_pct"] = df["GPs_with_Functional_CSC"] / df["No_of_GPs"] * 100
    # NOTE: Chandigarh & NCT of Delhi have 0 GPs -> ratio is NaN here.
    # Imputation is intentionally NOT done here to avoid data leakage.
    # It is done after the train/test split, using only the train median.
    return df


def train_model(df):
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # --- Impute missing GP coverage ratio AFTER the split, using only the
    # train set's median, to avoid leaking test-set information into training.
    train_median = X_train["Functional_Ratio_pct"].median()
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train["Functional_Ratio_pct"] = X_train["Functional_Ratio_pct"].fillna(train_median)
    X_test["Functional_Ratio_pct"] = X_test["Functional_Ratio_pct"].fillna(train_median)
    print(f"Train median used for imputation: {train_median:.2f}%")

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    print("=== Fitted Model ===")
    print(f"DigiLocker_Users = {model.coef_[0]:.2f} * CSC_Total "
          f"+ {model.coef_[1]:.2f} * GP_Coverage_Ratio + {model.intercept_:.2f}")

    print("\n=== Evaluation Metrics ===")
    print(f"Train R^2 : {model.score(X_train, y_train):.3f}")
    print(f"Test R^2  : {r2_score(y_test, y_pred_test):.3f}")
    print(f"Test MAE  : {mean_absolute_error(y_test, y_pred_test):,.0f}")
    print(f"Test RMSE : {np.sqrt(mean_squared_error(y_test, y_pred_test)):,.0f}")

    # Naive baseline for comparison
    baseline_pred = np.full_like(y_test, y_train.mean(), dtype=float)
    print(f"\nBaseline MAE  : {mean_absolute_error(y_test, baseline_pred):,.0f}")
    print(f"Baseline RMSE : {np.sqrt(mean_squared_error(y_test, baseline_pred)):,.0f}")

    return model, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test


def plot_actual_vs_predicted(y_train, y_pred_train, y_test, y_pred_test):
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    ax.scatter(y_train / 1e6, y_pred_train / 1e6, color="#94A3B8", alpha=0.7,
               s=45, label="Training set", edgecolor="black", linewidth=0.4)
    ax.scatter(y_test / 1e6, y_pred_test / 1e6, color="#E8730A", alpha=0.9,
               s=60, label="Test set (held-out)", edgecolor="black", linewidth=0.5)
    max_val = max(y_train.max(), y_test.max(), y_pred_test.max()) / 1e6 * 1.05
    ax.plot([0, max_val], [0, max_val], "r--", linewidth=1.5, label="Perfect prediction (y = x)")
    ax.set_xlabel("Actual DigiLocker Users (Millions)")
    ax.set_ylabel("Predicted DigiLocker Users (Millions)")
    ax.set_title("Predictive Model: Actual vs Predicted Demand", fontsize=13, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/chart6_actual_vs_predicted.png", dpi=150)
    plt.close()


def demand_scenario(model, df, state="Gujarat", csc_increase_pct=20):
    """Simulate a % increase in CSC infrastructure for a given state."""
    row = df[df["State"] == state][FEATURES].copy()
    boosted = row.copy()
    boosted["Functional_CSC_Total"] *= (1 + csc_increase_pct / 100)

    pred_now = model.predict(row)[0]
    pred_boost = model.predict(boosted)[0]
    increase = pred_boost - pred_now

    print(f"\n=== Demand Scenario: {state} (+{csc_increase_pct}% CSC) ===")
    print(f"Predicted demand now      : {pred_now:,.0f}")
    print(f"Predicted demand after    : {pred_boost:,.0f}")
    print(f"Projected increase        : {increase:,.0f}  ({increase / pred_now * 100:.2f}%)")


if __name__ == "__main__":
    data = load_data()
    model, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test = train_model(data)
    plot_actual_vs_predicted(y_train, y_pred_train, y_test, y_pred_test)
    demand_scenario(model, data, state="Gujarat", csc_increase_pct=20)
    print(f"\nChart saved -> {CHART_DIR}/chart6_actual_vs_predicted.png")
