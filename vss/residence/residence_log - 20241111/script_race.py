# Script to visualize racial trends by campus over the years

import pandas as pd
import matplotlib.pyplot as plt

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


# Filter data for each year on October 1st
october_1_data = {year: filter_october_1(df, year) for year, df in dfs.items()}

# Calculate racial distribution as percentages by campus on October 1 for each year
october_1_race_ratios = {
    year: data.groupby("CAMPUS_NAME")["RACE"].value_counts(normalize=True).unstack(fill_value=0) * 100
    for year, data in october_1_data.items()
}

# Combine racial data across years into a single DataFrame for plotting trends
combined_race_ratios_over_years = pd.concat(october_1_race_ratios, axis=0)
combined_race_ratios_over_years.index.names = ['Year', 'Campus']

# Plot racial trends by campus across years
for campus in combined_race_ratios_over_years.index.get_level_values('Campus').unique():
    campus_data = combined_race_ratios_over_years.xs(campus, level='Campus')

    plt.figure(figsize=(10, 6))
    for race in campus_data.columns:
        plt.plot(campus_data.index, campus_data[race], marker='o', label=race)

    # Chart details
    plt.title(f"Racial Trends for {campus} Campus Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Percentage (%)")
    plt.legend(title="Race")
    plt.grid(True)
    plt.show()
