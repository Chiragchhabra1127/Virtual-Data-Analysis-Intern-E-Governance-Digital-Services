# Virtual-Data-Analysis-Intern-E-Governance-Digital-Services
## Practical Code Files (Week 1–6)

**Author:** Chirag Chhabra

## Folder Structure
```
code_package/
├── data/
│   ├── RS_Session_265_AU_543_A_to_E_i.csv     (raw DigiLocker data)
│   └── state_wise-active__june-2026.xlsx       (raw CSC data)
├── charts/                                      (auto-created on run)
├── week1_strategic_planning.py
├── week2_data_collection_cleaning.py
├── week3_eda_visualization.py
├── week4_statistical_analysis.py
├── week5_predictive_modeling.py
├── week6_final_synthesis.py
├── requirements.txt
└── README.md
```

## How to Run

Install dependencies first:
```
pip install -r requirements.txt
```

Run scripts in order (each depends on the previous week's output):
```
python week1_strategic_planning.py
python week2_data_collection_cleaning.py   # creates data/merged_data.csv
python week3_eda_visualization.py           # creates charts/*.png
python week4_statistical_analysis.py
python week5_predictive_modeling.py         # creates charts/chart6_actual_vs_predicted.png
```

Or run everything end-to-end + get a final summary:
```
python week6_final_synthesis.py
```

## Data Sources
- DigiLocker Registered Users (State/UT-wise): https://data.gov.in/
- Common Service Centres (CSC), State-wise Active CSCs: https://csc.gov.in/
