from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
driver.get("https://www.teamusa.com/athletes")

# Wait for initial load
time.sleep(3)

# List of cities from the dataset
cities_df = pd.read_csv("uscities.csv")
cities_set = set(cities_df['city'].str.lower().tolist())

athletes = []
seen_athletes = set()

# Function to extract athletes data from the page source
def extract_athletes(page_source):
    wait = WebDriverWait(driver, 10)
    try:
      wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))  # Wait for all table rows to load
      soup = BeautifulSoup(page_source, "html.parser")
      for index, card in enumerate(soup.find_all("tr", class_="css-0")):
        if index == 0:
            continue  # Skip the first card
        #print(card)
        name = card.find("p", class_="chakra-text css-mpfnrl").text.strip()
        if name in seen_athletes:
            continue  # Skip if the athlete is already added
        p_tags = card.find_all("p", class_="chakra-text css-1c57jb4")
        hometown = p_tags[len(p_tags) - 1].text.strip()
        athletes.append({"Name": name, "Hometown": hometown})
        seen_athletes.add(name)  # Add to seen set
    except Exception as e:
        print()
        #print(f"Error: {e}")

# Extract data from the initial page
#extract_athletes(driver.page_source)

previous_scroll_height = 0
current_scroll_height = 1

# Click "Load More" until no more button appears
while True:

    #driver.execute_script("window.scrollBy(0, 1100);")
    #time.sleep(2)
    try:
        # Wait for the "Load more athletes" button to be clickable and click it
        previous_scroll_height = current_scroll_height
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loadMoreButtonId"]'))
        )
        load_more_button.click()
        time.sleep(3)  # Wait for new data to load
        current_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if current_scroll_height == previous_scroll_height:
          print("End of page detected.")
          print(current_scroll_height)
          print(previous_scroll_height)
          break
        #extract_athletes(driver.page_source)
        #print(driver.page_source)
    except:
        # Break the loop if there's no more button
        driver.execute_script("window.scrollBy(0, 500);")  # Adjust the value for scroll amount
        time.sleep(1)  # Allow page elements to adjust
        #break

extract_athletes(driver.page_source)

# Clean hometown data and merge with city dataset
athletes_df = pd.DataFrame(athletes)

# Add City and State to athletes_df only if Hometown is present
athletes_df['City'] = ''
athletes_df['State'] = ''

# Only process hometowns if present
for index, athlete in athletes_df.iterrows():
    if athlete['Hometown']:
        city, state = athlete['Hometown'].split(',') if ',' in athlete['Hometown'] else ('', '')
        athletes_df.at[index, 'City'] = city.strip()
        athletes_df.at[index, 'State'] = state.strip()

# Clean the "Hometown" column
for athlete in athletes:
    hometown = athlete.get("Hometown", "").lower()[:-4]
    if hometown not in cities_set:
        athlete["Hometown"] = ""

# Merge with city data for coordinates
merged_df = athletes_df.merge(cities_df, how='left', left_on=['City', 'State'], right_on=['city', 'state_id'])

# Save to CSV
merged_df.to_csv("team_usa_athletes_with_coords.csv", index=False)

driver.quit()