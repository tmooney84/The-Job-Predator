from confluent_kafka import Consumer, KafkaError
import json
import time
from sqlalchemy.exc import SQLAlchemyError
from models import Session, Quote

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

    try:
        while(True):
            msg = db_consumer.poll(10.0)
            if msg is None:
                print("Waiting...")
            
            elif msg.error():
                error_message = f"{time.ctime()}: ❌ Consumer error: {msg.error()}\n"
                print(error_message)
                with open("consumer_errors.log", "a") as error_log:
                    error_log.write(error_message)
                continue


            value = msg.value().decode('utf-8')
            data = json.loads(value)

            if data.get("type") == "done":
                print("✅ Done message received. Shutting down consumer.")
                break
            else:
                # Isolating each DB write to its own transaction/session
                try:
                    with Session() as session:
                        quote = Quote(text=data['text'], author=data['author'], tags=",".join(data['tags']))
                        session.add(quote)
                        session.commit()
                        print(f"✅ Consumed and inserted event: {data}")
                
                except SQLAlchemyError as e:
                    error_message = f"{time.ctime()}: ❌ Database error: {e}\n"
                    print(error_message)

                    with open("consumer_db_errors.log", "a") as error_log:
                        error_log.write(error_message)

    except KeyboardInterrupt:
        pass
    finally:
       db_consumer.close() 
       print("Consumer shutdown successfully")

if __name__=='__main__':
    run_consumer()