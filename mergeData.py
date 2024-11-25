import pandas as pd

# Load the Olympic athletes data from Excel
athletes_df = pd.read_excel('2020_US_Olympic_TeamAthletes_by_state.xlsx', engine='openpyxl')

if 'Name' in athletes_df.columns:
    # Split the Name column into First Name and Last Name
    athletes_df[['First Name', 'Last Name']] = athletes_df['Name'].str.split(' ', n=1, expand=True)
    # Drop the original Name column
    athletes_df = athletes_df.drop('Name', axis=1)

# Load the city coordinates data from CSV
cities_df = pd.read_csv('uscities.csv')

if 'Hometown' in athletes_df.columns:
    athletes_df[['Hometown', 'State']] = athletes_df['Hometown'].str.split(',', n=1, expand=True)
    athletes_df['Hometown'] = athletes_df['Hometown'].str.strip().str.title()
    athletes_df['State'] = athletes_df['State'].str.strip()

    #athletes_df = athletes_df.drop('Hometown', axis=1)


# Standardize column names for merging (adjust these to match your data)
#athletes_df.rename(columns={'Hometown City': 'Hometown', 'Hometown State': 'State'}, inplace=True)


# Merge the datasets on the 'City' column
merged_df = pd.merge(athletes_df, cities_df, left_on=['Hometown', 'State'], right_on=['city', 'state_name'], how='left')

filteredMerged_df = merged_df.filter(items=["First Name", "Last Name", "Sport", "Hometown", "State", "Gender", "state_id", "lat", "lng", "population"])

# Save the combined dataset to a new Excel file
filteredMerged_df.to_csv('2020combined_athletes.csv', index=False)