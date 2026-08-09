"""
Week 1 Task: Strategic Planning for E-Governance Data Analysis
----------------------------------------------------------------
This script performs an initial scan of the two raw data sources
to confirm their structure, size, and suitability before building
the strategic plan (Week 1 DOC report).

Data sources:
1. DigiLocker Registered Users (State/UT-wise) - data.gov.in
2. Common Service Centres (CSC) - State-wise Active CSCs, June 2026 - csc.gov.in
"""

import pandas as pd

DIGILOCKER_PATH = "data/RS_Session_265_AU_543_A_to_E_i.csv"
CSC_PATH = "data/state_wise-active__june-2026.xlsx"


def scan_digilocker():
    df = pd.read_csv(DIGILOCKER_PATH)
    print("=== DigiLocker Dataset (raw) ===")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(), "\n")
    return df


def scan_csc():
    # First look at the raw file without any header assumption
    raw = pd.read_excel(CSC_PATH, sheet_name=0, header=None)
    print("=== CSC Dataset (raw, no header) ===")
    print(raw.head(5), "\n")

    # Actual header is on the 2nd row (index 1)
    df = pd.read_excel(CSC_PATH, sheet_name=0, header=1)
    print("=== CSC Dataset (header=1) ===")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(), "\n")
    return df


if __name__ == "__main__":
    dl = scan_digilocker()
    csc = scan_csc()

    print("KEY PERFORMANCE INDICATORS IDENTIFIED:")
    print(" 1. Digital Adoption Rate  -> DigiLocker registered users")
    print(" 2. Service Infrastructure -> Functional CSC count (rural/urban)")
    print(" 3. Access Equity          -> % Gram Panchayats with functional CSC")
