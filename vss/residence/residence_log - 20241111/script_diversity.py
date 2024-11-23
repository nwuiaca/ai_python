import pandas as pd  # Make sure pandas is imported
import matplotlib.pyplot as plt
from datetime import datetime

# Analyze diversity target students who were offered residence placement but did not accept

# Load data (assuming dataframes `dfs` for each year are pre-loaded or loaded similarly)
file_paths = {
    "2019": "NWU Residence log 2019.xlsx",
    "2023": "NWU Residence log 2023.xlsx",
    "2024": "NWU Residence log 2024.xlsx"
}
dfs = {year: pd.read_excel(path) for year, path in file_paths.items()}

# Define criteria for diversity target groups (assuming specific race groups as an example)
diversity_targets = ["Black", "Coloured", "Asian"]


# Function to analyze placement offers and acceptances for diversity targets
def analyze_diversity_target_acceptance(df):
    # Filter students who are part of diversity targets
    target_students = df[df['RACE'].isin(diversity_targets)]

    # Calculate total offers and acceptance status
    total_offers = target_students.shape[0]
    accepted = target_students[target_students['FACCOMMCANCELCODEID'] == 0].shape[0]  # 0 indicates no cancellation
    rejected = total_offers - accepted  # Rejected offers are those with any cancellation reason

    # Return acceptance summary
    return {"Total Offers": total_offers, "Accepted": accepted, "Rejected": rejected}


# Analyze diversity target acceptance for each year
diversity_acceptance_summary = {year: analyze_diversity_target_acceptance(df) for year, df in dfs.items()}

# Combine results into a single DataFrame for easier output
output_df = pd.concat(diversity_acceptance_summary, names=["Year", "Campus"])

# Save the output to an Excel file
output_df.to_excel("Diversity_Acceptance_Summary.xlsx")

# Display the output DataFrame
print(output_df)
