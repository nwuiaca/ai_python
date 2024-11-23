import pandas as pd

# Load data
file_paths = {
    "2019": "NWU Residence log 2019.xlsx",
    "2023": "NWU Residence log 2023.xlsx",
    "2024": "NWU Residence log 2024.xlsx"
}
dfs = {year: pd.read_excel(path) for year, path in file_paths.items()}

# Define criteria for diversity target groups (assuming specific race groups as an example)
diversity_targets = ["Black", "Coloured", "Asian"]

# Update function to analyze placement offers and acceptances for diversity targets per campus
def analyze_diversity_target_acceptance_per_campus(df):
    # Filter students who are part of diversity targets
    target_students = df[df['RACE'].isin(diversity_targets)]

    # Group by campus and calculate offers, accepted, and rejected placements
    acceptance_summary = target_students.groupby("CAMPUS_NAME", group_keys=False).apply(lambda x: pd.Series({
        "Total Offers": x.shape[0],
        "Accepted": x[x['FACCOMMCANCELCODEID'] == 0].shape[0],  # Accepted offers have no cancellation
        "Rejected": x.shape[0] - x[x['FACCOMMCANCELCODEID'] == 0].shape[0]  # Remaining are rejected
    }))

    return acceptance_summary

# Analyze diversity target acceptance per campus for each year
diversity_acceptance_summary_per_campus = {year: analyze_diversity_target_acceptance_per_campus(df) for year, df in dfs.items()}

# Combine results into a single DataFrame for easier output
output_df = pd.concat(diversity_acceptance_summary_per_campus, names=["Year", "Campus"])

# Save the output to an Excel file
output_df.to_excel("Diversity_Acceptance_Summary_Per_Campus.xlsx")

# Display the output DataFrame
print(output_df)
