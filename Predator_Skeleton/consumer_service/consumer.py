from kafka import KafkaConsumer
import json
from models import Session, Quote

json_consumer = KafkaConsumer(
    'json_topic',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
csv_consumer = KafkaConsumer(
    'json_topic',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
session = Session()

#need infinite while loop to pandas
#put on schedule to start at 11:59 or timeout after certain time
while(True):
    # for message in json_consumer:
    #     #if no message in csv_comsumer, wait(10 seconds) try again and then continue
    #     #continue if need to retry loop if the retry is unsuccess (maybe break) 
    #     json_data = message.value
    #     # data = json_pandas(json_data) fn back to here?
    #     quote = Quote(text=data['text'], author=data['author'], tags=",".join(data['tags']))
    #     session.add(quote)
    #     session.commit()

    for message in csv_consumer:
        #if no message in csv_comsumer, wait(10 seconds) try again and then continue
        #continue if need to retry loop if the retry is unsuccess (maybe break) 
        csv_data = message.value

        csv_to_db_pandas(csv_data) 
       
       
        #data = csv_to_db_pandas(csv_data) fn back to here?
        #quote = Quote(text=data['text'], author=data['author'], tags=",".join(data['tags']))
        #session.add(quote)
        #session.commit()
