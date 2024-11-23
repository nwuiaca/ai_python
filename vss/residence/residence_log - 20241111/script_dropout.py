import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data
file_paths = {
    "2019": "NWU Residence log 2019.xlsx",
    "2023": "NWU Residence log 2023.xlsx",
    "2024": "NWU Residence log 2024.xlsx"
}
dfs = {year: pd.read_excel(path) for year, path in file_paths.items()}


# Function to filter students present on specific dates
def filter_date(df, date):
    return df[(df['STARTDATE'] <= date) & (df['ENDDATE'] >= date)].copy()


# Calculate age based on date of birth
def calculate_age(dob, ref_date):
    return ref_date.year - dob.year - ((ref_date.month, ref_date.day) < (dob.month, dob.day))


# Prepare data: filter on January 1 and October 1, calculate age, and identify dropouts
october_1_data = {}
dropout_analysis = {}

for year, df in dfs.items():
    # Convert year to integer
    ref_date_january = datetime(int(year), 1, 1)
    ref_date_october = datetime(int(year), 10, 1)

    # Filter students present on January 1 and calculate age
    in_january = filter_date(df, ref_date_january.strftime('%Y-%m-%d'))
    in_january['AGE'] = in_january['DATEOFBIRTH'].apply(lambda dob: calculate_age(dob, ref_date_january))

    # Filter students not present on October 1 (dropouts)
    not_in_october = filter_date(df, ref_date_october.strftime('%Y-%m-%d'))
    dropouts = in_january[~in_january['STUDENT'].isin(not_in_october['STUDENT'])]

    # Dropout counts and reasons by campus
    dropout_counts = dropouts.groupby("CAMPUS_NAME").size()
    reasons = dropouts.groupby("CAMPUS_NAME")['CANCELLATION_REASON'].value_counts()

    # Store the dropout analysis for each year
    dropout_analysis[year] = (dropout_counts, reasons)

# Display the dropout counts and reasons for each year
for year, (counts, reasons) in dropout_analysis.items():
    print(f"Dropout Analysis for {year}")
    print("Dropout Counts by Campus:")
    print(counts)
    print("\nDropout Reasons by Campus:")
    print(reasons)
    print("\n" + "-" * 50 + "\n")
