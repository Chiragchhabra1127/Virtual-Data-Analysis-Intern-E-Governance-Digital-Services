"""
Week 2 Task: Data Collection and Cleaning for Digital Services
----------------------------------------------------------------
Extracts, cleans, standardizes, and merges the two raw datasets into
one validated combined dataset covering 36 states/UTs.

Output: data/merged_data.csv
"""

import pandas as pd

DIGILOCKER_PATH = "data/RS_Session_265_AU_543_A_to_E_i.csv"
CSC_PATH = "data/state_wise-active__june-2026.xlsx"
OUTPUT_PATH = "data/merged_data.csv"

# Known naming mismatches between the two sources -> standardized key
NAME_FIXES = {
    "DADRA & NH, D&D": "DADRA AND NAGAR HAVELI AND DAMAN AND DIU",
    "DELHI": "NCT OF DELHI",
}


def load_digilocker():
    df = pd.read_csv(DIGILOCKER_PATH)
    df.columns = ["SlNo", "State", "DigiLocker_Users"]
    df["key"] = df["State"].str.upper().str.strip()
    return df


def load_csc():
    # header=1 because row 0 is a report title, not column names
    df = pd.read_excel(CSC_PATH, sheet_name=0, header=1)
    df.columns = [
        "State", "Functional_CSC_Total", "Functional_CSC_Rural",
        "Functional_CSC_Urban", "No_of_GPs",
        "GPs_with_Registered_CSC", "GPs_with_Functional_CSC",
    ]
    # Drop the national 'TOTAL' summary row
    df = df[df["State"] != "TOTAL"].copy()
    df["key"] = df["State"].str.upper().str.strip()
    df["key"] = df["key"].replace(NAME_FIXES)
    return df


def clean_and_merge():
    dl = load_digilocker()
    csc = load_csc()

    # --- Data quality checks ---
    print("Missing values (DigiLocker):\n", dl.isnull().sum())
    print("Missing values (CSC):\n", csc.isnull().sum())
    print("Duplicate states (DigiLocker):", dl["key"].duplicated().sum())
    print("Duplicate states (CSC):", csc["key"].duplicated().sum())

    # --- Merge on standardized key ---
    merged = pd.merge(dl, csc, on="key", suffixes=("_dl", "_csc"))
    merged = merged.drop(columns=["key", "SlNo", "State_csc"])
    merged = merged.rename(columns={"State_dl": "State"})

    # --- Enforce numeric types ---
    numeric_cols = [
        "DigiLocker_Users", "Functional_CSC_Total", "Functional_CSC_Rural",
        "Functional_CSC_Urban", "No_of_GPs", "GPs_with_Registered_CSC",
        "GPs_with_Functional_CSC",
    ]
    for col in numeric_cols:
        merged[col] = pd.to_numeric(merged[col], errors="coerce").astype("Int64")

    print("\nFinal merged dataset shape:", merged.shape)
    print(merged.head())

    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved cleaned & merged dataset -> {OUTPUT_PATH}")
    return merged


if __name__ == "__main__":
    clean_and_merge()
