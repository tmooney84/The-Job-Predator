import schedule
import time
from kafka import KafkaProducer
import json
#from scraper_orchestrator import ibm_scraper
from scrapers import site1_scraper  # Import your scraper modules
from scrapers import site2_scraper  # Import your scraper modules

json_scraper_list = [site1_scraper, site2_scraper]
csv_scraper_list = [site1_scraper, site2_scraper]

producer1 = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def run_all_scrapers():
    for scraper in json_scraper_list:
        data = scraper.scrape()
        for item in data:
            producer.send('json_topic', item)
    producer.flush()

    for scraper in csv_scraper_list:
        data = scraper.scrape()
        for item in data:
            producer.send('csv_topic', item)
    producer.flush()

# need to gracefully handle scraper exceptions

schedule.every().day.at("00:00").do(run_all_scrapers)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)

