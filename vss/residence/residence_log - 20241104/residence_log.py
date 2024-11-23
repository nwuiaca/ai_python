import pandas as pd

# Load your Excel file
data = pd.read_excel('01 NWU Residence 2019.xlsx')

# Ensure dates are in datetime format
data['STARTDATE'] = pd.to_datetime(data['STARTDATE'])
data['ENDDATE'] = pd.to_datetime(data['ENDDATE'])

# Group by 'STUDENT' and 'RESIDENCE', then aggregate to get minimum STARTDATE and maximum ENDDATE
consolidated_per_residence = data.groupby(['STUDENT', 'RESIDENCE']).agg(
    BEGIN_DATE=('STARTDATE', 'min'),
    END_DATE=('ENDDATE', 'max')
).reset_index()

# Export the consolidated data to a new Excel file
consolidated_per_residence.to_excel('02 Consolidated_Student_Residence.xlsx', index=False)

# Ensure dates are in datetime format
consolidated_per_residence['BEGIN_DATE'] = pd.to_datetime(consolidated_per_residence['BEGIN_DATE'])
consolidated_per_residence['END_DATE'] = pd.to_datetime(consolidated_per_residence['END_DATE'])

# Count the number of unique residences per student
residence_count = consolidated_per_residence.groupby('STUDENT')['RESIDENCE'].nunique()

# Identify students who stayed in only one residence and those who moved
single_residence_students = residence_count[residence_count == 1].index
moved_residence_students = residence_count[residence_count > 1].index

# Filter the consolidated data for students who did not move
consolidated_no_moves = consolidated_per_residence[consolidated_per_residence['STUDENT'].isin(single_residence_students)]

# Further filter to find students who stayed the full term (END_DATE in October or later) and those who left early (END_DATE before October)
full_term_students = consolidated_no_moves[consolidated_no_moves['END_DATE'].dt.month >= 10]
left_before_october = consolidated_no_moves[consolidated_no_moves['END_DATE'].dt.month < 10]

# Filter for students who moved residences
students_moved_data = consolidated_per_residence[consolidated_per_residence['STUDENT'].isin(moved_residence_students)]

# Export all lists to separate Excel files
consolidated_no_moves.to_excel('04 Consolidated_Student_Residence_No_Moves.xlsx', index=False)
students_moved_data.to_excel('03 Students_Moved_Residences.xlsx', index=False)
full_term_students.to_excel('05 Full_Term_Students_No_Moves.xlsx', index=False)
left_before_october.to_excel('06 Left_Before_October_No_Moves.xlsx', index=False)

