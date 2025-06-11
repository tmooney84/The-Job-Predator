import json
import socket
import time
import logging
from confluent_kafka import Producer
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
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

    # def run_all_scrapers(self):
    #     # TODO: Test to see if dropping into subprocess is more efficient at
    #     #       scale given the changes to the Selenium logic's UUIDs to be
    #     #       unique;; if using ThreadPools need to limit to between 
    #     #       ***3 - 10
    #     #       threads at the same time is all we can handle for selenium
    #     #       Python threads per batch to conserve cpu resources at scale
        
    #     with ThreadPoolExecutor(max_workers=len(self.csv_scrapers)) as executor:
    #         executor.map(self.run_scraper, self.csv_scrapers)

    #     # Send 'done' message
    #     self.producer.produce(
    #         topic=self.topic,
    #         value=json.dumps({"type": "done"}),
    #         callback=self.delivery_report
    #     )
    #     self.producer.flush()

    def worker(self, scraper_queue):
        while not scraper_queue.empty():
            scraper = scraper_queue.get()
            try:
                self.run_scraper(scraper)
            except Exception as e:
                print(f"Scrape failed: {e}")
            scraper_queue.task_done()

    def run_all_scrapers(self):
        # Limited the available threads to 5 because Selenium is a heavy process 
        # that will be used by the majority of our scrapers. Each thread will 
        # concurrently pull scrape jobs from a shared queue. When we have more computing 
        # power can increase the number of threads to be run concurrently.

        scraper_queue = Queue()

        for scraper in self.csv_scrapers:
            scraper_queue.put(scraper)

        with ThreadPoolExecutor(max_workers= 5) as executor:
            for _ in range(5):
                executor.submit(self.worker, scraper_queue)

        scraper_queue.join()

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
