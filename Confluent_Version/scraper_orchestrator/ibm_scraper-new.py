from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchAttributeException
import json
import re

driver = webdriver.Chrome()
driver.get("https://www.ibm.com/careers/search?field_keyword_08%5B0%5D=Consulting&field_keyword_08%5B1%5D=Enterprise%20Operations&field_keyword_08%5B2%5D=Infrastructure%20%26%20Technology&field_keyword_08%5B3%5D=Software%20Engineering&field_keyword_05%5B0%5D=United%20States")

wait = WebDriverWait(driver, 20)
page_sources = []

# Wait for initial load
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bx--card__wrapper")))

while True:
    # Save the current page source
    page_sources.append(driver.page_source)

    try:
        # Locate "Next" button
        next_button = wait.until(
            EC.presence_of_element_located((By.ID, "IBMAccessibleItemComponents-next"))
        )

        # Check if button is visible and enabled
        if not next_button.is_displayed() or not next_button.is_enabled():
            print("Next button is disabled or hidden. Stopping.")
            break

        # Scroll to button and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Wait for new content to load by detecting job card count change
        previous_count = len(driver.find_elements(By.CLASS_NAME, "bx--card__wrapper"))
        for _ in range(10):
            time.sleep(1)
            new_count = len(driver.find_elements(By.CLASS_NAME, "bx--card__wrapper"))
            if new_count > previous_count:
                break
        else:
            print("No new jobs loaded. Assuming last page.")
            break

    except Exception as e:
        print("Error or no more pages:", e)
        break

driver.quit()

page_source = ''.join(page_sources)
soup = BeautifulSoup(page_source, 'html.parser')

job_cards = soup.find_all('div', class_="bx--card-group__cards__col")

import re

jobs = {
    'title': [],
    'location': [],
    'link' : []
}

pattern = r"^(Entry Level|Professional)"

for card in job_cards:
    raw_location = card.div.div.div.find('div', class_="ibm--card__copy__inner").text.strip()

    # Match experience level safely
    match = re.match(pattern, raw_location, flags=re.IGNORECASE)
    if match:
        experience_level = match.group(1)
        location = raw_location.replace(experience_level, '').strip()
    else:
        experience_level = "Unknown"
        location = raw_location  # leave full string as location
    jobs['link'].append(card.a['href'])
    jobs['title'].append(card['aria-label'])
    jobs['category'].append(card.div.div.div.div.text.strip())
    jobs['location'].append(location)
    jobs['experience_level'].append(experience_level)

#######!!! print worked once an has had trouble since
print(json.dumps(jobs, indent=2))