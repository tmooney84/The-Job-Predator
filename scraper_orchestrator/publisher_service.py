import json
import socket
import time
import logging
from confluent_kafka import Producer
from concurrent.futures import ThreadPoolExecutor
from scrapers import site1_scraper, site2_scraper  # import scraper modules

class Publisher:
    def __init__(self):
        self.csv_scrapers = [site1_scraper, site2_scraper]
        self.conf = {
            'acks': 'all',
            'bootstrap.servers': 'kafka1:19091',
            'client.id': socket.gethostname()
        }
        self.producer = Producer(self.conf)
        self.topic = "sql_queue"

        # Logging setup
        logging.basicConfig(filename="publisher_service.log", level=logging.INFO, format='%(asctime)s | %(message)s')

    def delivery_report(self, err, msg):
        if err is not None:
            logging.error(f"FAILED DELIVERY: {err}")
        else:
            decoded_value = msg.value().decode('utf-8')
            logging.info(
                f"Produced event to topic {msg.topic()}: partition={msg.partition()}, value={decoded_value}"
            )

    def run_scraper(self, scraper_module):
        scraper_name = scraper_module.__name__
        logging.info(f"Running scraper: {scraper_name}")

        try:
            results = scraper_module.scrape()
            for item in results:
                self.producer.produce(
                    topic=self.topic,
                    value=json.dumps(item),
                    callback=self.delivery_report
                )
        except Exception as e:
            error_msg = f"Error running scraper {scraper_name}: {e}"
            logging.error(error_msg)
            with open("scraper_errors.log", "a") as error_log:
                error_log.write(f"{time.ctime()}: {error_msg}\n")

    def run_all_scrapers(self):
        with ThreadPoolExecutor(max_workers=len(self.csv_scrapers)) as executor:
            executor.map(self.run_scraper, self.csv_scrapers)

        # Send 'done' message
        self.producer.produce(
            topic=self.topic,
            value=json.dumps({"type": "done"}),
            callback=self.delivery_report
        )
        self.producer.flush()

if __name__ == "__main__":
    publisher = Publisher()
    publisher.run_all_scrapers()
    print("done!")
