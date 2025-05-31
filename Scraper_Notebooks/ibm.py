from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re
import random

# Set up WebDriver
driver = webdriver.Chrome()
driver.get("https://www.ibm.com/careers/search?field_keyword_08%5B0%5D=Consulting&field_keyword_08%5B1%5D=Enterprise%20Operations&field_keyword_08%5B2%5D=Infrastructure%20%26%20Technology&field_keyword_08%5B3%5D=Software%20Engineering&field_keyword_05%5B0%5D=United%20States")

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bx--card__wrapper")))

page_source = []

while True:
    page_source.append(driver.page_source)
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "IBMAccessibleItemComponents-next")))
        driver.execute_script("arguments[0].click();", next_button)

        #time.sleep(3)
        time.sleep(random.randint(1,5))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bx--card__wrapper")))
    except:
        print("No more pages.")
        break

driver.quit()

page_source = ''.join(page_source)
soup = BeautifulSoup(page_source, 'html.parser')
job_cards = soup.find_all('div', class_="bx--card-group__cards__col")

pattern = r"^(Entry Level|Professional)"
jobs_list = []

for card in job_cards:
    try:
        raw_location = card.div.div.div.find('div', class_="ibm--card__copy__inner").text.strip()
    except AttributeError:
        raw_location = "Unknown"

    match = re.match(pattern, raw_location, flags=re.IGNORECASE)
    experience_level = match.group(1) if match else "Unknown"
    location = raw_location.replace(experience_level, '').strip() if match else raw_location

    job_data = {
        'company': 'IBM',
        'title': card.get('aria-label', 'Unknown'),
        'category': card.div.div.div.div.text.strip() if card.div.div.div.div else 'Unknown',
        'location': location,
        'experience_level': experience_level,
        'link': card.a['href'] if card.a else 'No link found'
    }

    jobs_list.append(job_data)

    # Print job JSON to terminal
    print(json.dumps(job_data, indent=2))

# Optionally convert to DataFrame if needed later
# df = pd.DataFrame(jobs_list)
