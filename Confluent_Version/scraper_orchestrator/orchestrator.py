import schedule
import time
import json
import socket
from confluent_kafka import Producer
from consumer_service.consumer import run_consumer

from scrapers import site1_scraper, site2_scraper  # Import scraper modules

#json_scraper_list = [json1_scraper, json2_scraper]
#api_list = [api1, api2]

csv_scrapers = [site1_scraper, site2_scraper]

conf = {
    'bootstrap.servers': 'localhost:9091',
    'client.id': socket.gethostname()
}

producer = Producer(conf)
topic = "sql_queue"

def delivery_report(err, msg):
    log_entry = ""
    if err is not None:
        log_entry = f"FAILED DELIVERY: {err}\n"
    else:
        log_entry = (
            f"{time.ctime()} | Produced event to topic {msg.topic()}: "
            f"partition = {msg.partition():<4} "
            f"value = {msg.value()}\n"
            ##f"partition = {msg.partition().decode('utf-8'):12}"
            ##f"value = {json.loads(msg.value()).decode('utf-8')}\n"
        )
    
    with open("producer_log.txt", "a") as log_file:
        log_file.write(log_entry)

def run_all_scrapers():
    for scraper in csv_scrapers:
        try:
            data = scraper.scrape()
            for item in data:
           ##########!!!BRING IN PANDAS into json 
                producer.produce(topic=topic,value=json.dumps(item), callback=delivery_report)
        except Exception as e:
            print(f"Error running scraper {scraper}: {e}")
            with open("scraper_errors.log", "a") as error_log:
                error_log.write(f"{time.ctime()}: Error running scraper {scraper}: {e}\n") 

    # Send 'done' message at the end
    producer.produce(topic=topic, value=json.dumps({"type": "done"}), callback=delivery_report)
    
    producer.flush()

schedule.every().day.at("00:00").do(run_consumer)
schedule.every().day.at("00:00").do(run_all_scrapers)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)

