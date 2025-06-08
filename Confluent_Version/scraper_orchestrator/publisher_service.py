import schedule
import time
import json
import socket
from confluent_kafka import Producer
import subprocess
import sys

class Publisher:
    csv_scrapers = [
        "scrapers/site1_scraper.py",
        "scrapers/site2_scraper.py"
    ]
    conf = {
        'acks': 'all',
        'bootstrap.servers': 'kafka1:19091',
        'client.id': socket.gethostname()
    }

    producer = Producer(conf)
    topic = "sql_queue"

    @staticmethod
    def delivery_report(err, msg):
        log_entry = ""
        if err is not None:
            log_entry = f"FAILED DELIVERY: {err}\n"
        else:
            log_entry = f"{time.ctime()} | Produced event to topic {msg.topic()}:\
                partition = {msg.partition():12} \n \
                value = {msg.value().decode('utf-8')}\
                value = {json.loads(msg.value())}"
        with open("publisher_service.log", "a") as log_file:
            print('entered {} into db', log_entry)
            log_file.write(log_entry)

    def run_all_scrapers(self):
        for scraper_script in self.csv_scrapers:
            try:
                print(f"Running scraper: {scraper_script}")
                # Launch scraper as a separate process
                result = subprocess.run([sys.executable, scraper_script], capture_output=True, text=True, check=True)

                # Process the output
                output_lines = result.stdout.strip().splitlines()
                for line in output_lines:
                    try:
                        item = json.loads(line)
                        self.producer.produce(topic=self.topic, value=json.dumps(item), callback=self.delivery_report)
                    except json.JSONDecodeError:
                        # Skip lines that aren't JSON (like print statements)
                        continue

            except subprocess.CalledProcessError as e:
                print(f"Error running scraper {scraper_script}: {e}")
                with open("scraper_errors.log", "a") as error_log:
                    error_log.write(f"{time.ctime()}: Error running scraper {scraper_script}: {e}\n")

        # Send 'done' message at the end
        self.producer.produce(topic=self.topic, value=json.dumps({"type": "done"}), callback=self.delivery_report)
        self.producer.flush()

if __name__ == "__main__":
    run_publisher = Publisher()
    run_publisher.run_all_scrapers()
    print('done!')
