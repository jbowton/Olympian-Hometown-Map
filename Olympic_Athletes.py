import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.teamusa.com/athletes"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

athletes = []
for card in soup.find_all("tr", class_="css-0"):
    name = card.find("p", class_= "chakra-text css-mpfnrl").text.strip()
    p_tags = card.find_all("p", class_="chakra-text css-1qjehc2")
    hometown = p_tags[len(p_tags) - 1].text.strip()
    athletes.append({"Name": name, "Hometown": hometown})

cities_df = pd.read_csv("uscities.csv")

# List of cities from the dataset
cities_list = cities_df['city'].str.lower().tolist()
# Convert to set for faster look up
cities_set = set(cities_list)

# Iterate over athletes' hometown and check if the hometown is valid
for athlete in athletes:
    hometown = athlete.get("Hometown", "").lower()
    if hometown not in cities_set:
        athlete["Hometown"] = ""

# Save to CSV
df = pd.DataFrame(athletes)
df.to_csv("team_usa_athletes.csv", index=False)
