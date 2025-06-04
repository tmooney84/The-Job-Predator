from kafka import KafkaConsumer
import json
import time
from models import Session, Quote

###remember json.loads(value_str) >>> will load json string to python
# object

def run_consumer():

    dbq_config = {
        'bootstrap.servers': 'localhost:9091', # minimum need
        'group.id': 'sql-group',
        'client.id': 'sql-db-consumer-1', # minimum need
        ###!!! 
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'}
        ###!!! 
    }

    db_consumer = Consumer(dbq_config)
    topic = "sql_queue"
    db_consumer.subscribe([topic])
    print(f"{time.ctime()} Consumer started.")

###!!!
    session = Session()

###???put on schedule to start at 11:59 or timeout after certain time
    try:
        while(True):
            msg = db_consumer.poll(10.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            value = msg.value().decode('utf-8')
            data = json.loads(value)

            if data.get("type") == "done":
                print("✅ Done message received. Shutting down consumer.")
                break  # exit the loop and shut down
            else:
                print(f"Consumed event: {data}")


        # for message in json_consumer:
        #     #if no message in csv_comsumer, wait(10 seconds) try again and then continue
        #     #continue if need to retry loop if the retry is unsuccess (maybe break) 
        #     json_data = message.value
        #     # data = json_pandas(json_data) fn back to here?
        #     quote = Quote(text=data['text'], author=data['author'], tags=",".join(data['tags']))
        #     session.add(quote)
        #     session.commit()

            for message in db_consumer:
        #if no message in csv_comsumer, wait(10 seconds) try again and then continue
        #continue if need to retry loop if the retry is unsuccess (maybe break) 
                csv_data = message.value

                csv_to_db_pandas(csv_data) 
       
       
        #data = csv_to_db_pandas(csv_data) fn back to here?
        #quote = Quote(text=data['text'], author=data['author'], tags=",".join(data['tags']))
        #session.add(quote)
        #session.commit()

        ###???should this go above db stuff?
    except KeyboardInterrupt:
        pass
    finally:
       db_consumer.close() 
       print("Consumer shutdown successfully")

if __name__=='__main__':
    run_consumer()