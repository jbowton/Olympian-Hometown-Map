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
    #if len(p_tags) == 4:
      #hometown = p_tags[3].text.strip()  # Adjust as needed
    #elif len(p_tags) == 3:
       #hometown = p_tags[2].text.strip()
    hometown = p_tags[len(p_tags) - 1].text.strip()
    athletes.append({"Name": name, "Hometown": hometown})
    print(p_tags)

# Save to CSV
df = pd.DataFrame(athletes)
df.to_csv("team_usa_athletes.csv", index=False)
