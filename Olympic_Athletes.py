import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.teamusa.com/athletes"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

cities_df = pd.read_csv("uscities.csv")

athletes = []
for card in soup.find_all("tr", class_="css-0"):
    name = card.find("p", class_= "chakra-text css-mpfnrl").text.strip()
    p_tags = card.find_all("p", class_="chakra-text css-1qjehc2")
    hometown = p_tags[len(p_tags) - 1].text.strip()
    athletes.append({"Name": name, "Hometown": hometown})

# List of cities from the dataset
cities_list = cities_df['city'].str.lower().tolist()
# Convert to set for faster look up
cities_set = set(cities_list)

#states_list = cities_df['state_id'].st

# Iterate over athletes' hometown and check if the hometown is valid
for athlete in athletes:
    #Remove state code for check
    hometown = athlete.get("Hometown", "").lower()[:-4]
    if hometown not in cities_set:
        athlete["Hometown"] = ""

# Save to CSV
athletes_df = pd.DataFrame(athletes)
#Merge athlete to city data
athletes_df[['City', 'State']] = athletes_df['Hometown'].str.split(',', expand=True)
athletes_df['State'] = athletes_df['State'].str.strip()  # Remove extra spaces
merged_df = athletes_df.merge(cities_df, how='left', left_on=['City', 'State'], right_on=['city', 'state_id'])

# Save the updated dataframe to CSV
merged_df.to_csv("team_usa_athletes_with_coords.csv", index=False)
#df.to_csv("team_usa_athletes.csv", index=False)
