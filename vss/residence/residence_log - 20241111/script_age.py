# Script to visualize average age trends by campus over the years

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data (assuming dataframes `dfs` for each year are pre-loaded or loaded similarly)
file_paths = {
    "2019": "NWU Residence log 2019.xlsx",
    "2023": "NWU Residence log 2023.xlsx",
    "2024": "NWU Residence log 2024.xlsx"
}
dfs = {year: pd.read_excel(path) for year, path in file_paths.items()}

# Function to filter students present on October 1st of each year
def filter_october_1(df, year):
    october_1 = f"{year}-10-01"
    return df[(df['STARTDATE'] <= october_1) & (df['ENDDATE'] >= october_1)]

# Calculate age based on date of birth
def calculate_age(dob, ref_date):
    return ref_date.year - dob.year - ((ref_date.month, ref_date.day) < (dob.month, dob.day))

# Process data to include age on October 1st for each year with warning fixed
october_1_data = {}
for year, df in dfs.items():
    ref_date = datetime(int(year), 10, 1)  # Convert year to integer
    df_filtered = filter_october_1(df, int(year)).copy()  # Use .copy() to avoid SettingWithCopyWarning
    df_filtered['AGE'] = df_filtered['DATEOFBIRTH'].apply(lambda dob: calculate_age(dob, ref_date))
    october_1_data[year] = df_filtered

# Calculate average age by campus for each year on October 1st
october_1_age_trends = {
    year: data.groupby("CAMPUS_NAME")["AGE"].mean() for year, data in october_1_data.items()
}

# Combine average age data across years for each campus into a single DataFrame for plotting trends
combined_age_trends_over_years = pd.DataFrame(october_1_age_trends)

# Plot average age trends by campus across years
plt.figure(figsize=(10, 6))
for campus in combined_age_trends_over_years.index:
    plt.plot(combined_age_trends_over_years.columns, combined_age_trends_over_years.loc[campus], marker='o', label=campus)

# Chart details
plt.title("Average Age Trends by Campus Over the Years (October 1st)")
plt.xlabel("Year")
plt.ylabel("Average Age")
plt.legend(title="Campus")
plt.grid(True)
plt.show()
