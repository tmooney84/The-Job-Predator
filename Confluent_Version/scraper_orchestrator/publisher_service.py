import schedule
import time
import json
import socket
from confluent_kafka import Producer

from scrapers import site1_scraper, site2_scraper  # Import scraper modules

#json_scraper_list = [json1_scraper, json2_scraper]
#api_list = [api1, api2]
def run_publisher():
    csv_scrapers = [site1_scraper, site2_scraper]
    conf = {
        'acks': 'all',
        'bootstrap.servers': 'kafka1:19091',
        'client.id': socket.gethostname()
    }

    producer = Producer(conf)
    topic = "sql_queue"

    def delivery_report(err, msg):
        log_entry = ""
        if err is not None:
            log_entry = f"FAILED DELIVERY: {err}\n"
        else:
            log_entry = f"{time.ctime()} | Produced event to topic {msg.topic()}:\
                partition = {msg.partition().decode('utf-8'):12} \n \
                value = {msg.value().decode('utf-8')}\
                value = {json.loads(msg.value()).decode('utf-8')}"
                
        with open("app/scraper_orchestrator/publisher_service.log", "a") as log_file:
            print('entered {} into db', log_entry)
            log_file.write(log_entry)
        
    def run_all_scrapers(): #daily_scrape_job()
        for scraper in csv_scrapers:
            try:
                data = scraper.scrape()
                for item in data:
               ##########!!!BRING IN PANDAS into json
                    producer.produce(topic=topic,value=json.dumps(item), callback=delivery_report)
            except Exception as e:
                print(f"Error running scraper {scraper}: {e}")
                with open("app/scraper_orchestrator/scraper_errors.log", "a") as error_log:
                    error_log.write(f"{time.ctime()}: Error running scraper {scraper}: {e}\n")

        # Send 'done' message at the end
        producer.produce(topic=topic, value=json.dumps({"type": "done"}), callback=delivery_report)
        #TODO: add single scraper that does a 'full run'
        producer.flush()


if __name__ == "__main__":
    run_publisher()
    print('done!')
