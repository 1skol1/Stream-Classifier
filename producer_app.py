import datetime
import os
import uuid

import uvicorn
from fastapi import FastAPI, File

from unified import kafka, pubsub
from utils import *

app = FastAPI()


app.kf = kafka({
    "bootstrap.servers": "localhost:9092"
    })
credentials_path = 'service-account-info.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
app.ps = pubsub(os.getenv('GOOGLE_CLOUD_PROJECT'),'fashion-mnist-pubsub-stream')


@app.on_event("startup")
async def startup_event():
    
    app.kf.create_topic(['fashion-mnist-kafka-stream'],1,3)
    app.ps.create_topic()
    
    
    
@app.post('/kafka-predict', status_code=200)
async def predict_kafka(file: bytes = File(...)):
    """ FastAPI 
    Args:
        file (bytes): fashion-mnist image 
    Returns:
        None

    """

    producer = app.kf.kafka_produce()
    producer.poll(0)
    producer.produce(
                    topic='fashion-mnist-kafka-stream', 
                    value=file, 
                    callback=delivery_report,
                    timestamp=int(datetime.datetime.now().timestamp()),
                    headers={
                        "video_id": uuid.uuid4().hex.encode("utf-8")
                    }
                )
    producer.flush()


@app.post('/pubsub-predict', status_code=200)
async def predict_pubsub(file: bytes = File(...)):

    
    custom_retry = app.ps.get_custom_retry()
    video_id = uuid.uuid4().hex.encode("utf-8")
    producer,topic_name = app.ps.pubsub_produce()
    future = producer.publish(topic_name,file,video_id=video_id,timestamp=str(datetime.datetime.now().timestamp()),retry=custom_retry)
    future.result()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
