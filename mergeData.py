import pandas as pd

# Load the Olympic athletes data from Excel
athletes_df = pd.read_excel('Olympic_roster2024.xlsx', engine='openpyxl')

# Load the city coordinates data from CSV
cities_df = pd.read_csv('uscities.csv')

# Standardize column names for merging (adjust these to match your data)
athletes_df.rename(columns={'Hometown City': 'Hometown', 'Hometown State': 'State'}, inplace=True)

# Ensure proper casing and remove extra spaces
athletes_df['Hometown'] = athletes_df['Hometown'].str.strip().str.title()
cities_df['city'] = cities_df['city'].str.strip().str.title()

# Merge the datasets on the 'City' column
merged_df = pd.merge(athletes_df, cities_df, left_on=['Hometown', 'State'], right_on=['city', 'state_name'], how='left')

filteredMerged_df = merged_df.filter(items=["First Name", "Last Name", "Sport", "Hometown", "State", "Gender", "state_id", "lat", "lng", "population"])

# Save the combined dataset to a new Excel file
filteredMerged_df.to_csv('combined_athletes_data.csv', index=False)