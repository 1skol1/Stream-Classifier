import io

import numpy as np
import argparse
import PIL.Image as Image
from pymongo import MongoClient

from tf_helper import get_model_prediction, get_stub
from unified import kafka
from utils import *


class ConsumerThread:
    def __init__(self, topic, db,host):

        self.topic = topic
        self.db = db
        self.host = host
        self.collection = self.db['test_collection']
        self.consumer = kafka.kafka_consumer(self.topic)
        self.run(self.consumer)

        
    def run(self, consumer):
        try:
            while True:
                msg = consumer.poll(0.5)
                if msg == None:
                    continue
                elif msg.error() == None:

                    # convert image bytes data to numpy array of dtype uint8
                    
                    image = Image.open(io.BytesIO(msg.value()))
                    
                    # get metadata
                    timestamp = msg.timestamp()[1]
                    frame_no = msg.headers()[0][1].decode("utf-8")
 
                    image = np.array(image)
                    image = np.reshape(image, image.shape + (1,))
                    #model request
                    stub = get_stub(self.host)
                    print("\nCreate RPC connection ...")
                    model_prediction = get_model_prediction(image, stub)
                    #
                    # insert results into mongodb
                    doc = {
                                "frame_id": frame_no,
                                "timestamp": timestamp,
                                "label": model_prediction
                           }
                    self.collection.insert_one(doc)

                    # commit synchronously
                    consumer.commit(asynchronous=False)


                else:
                    kafka.EOF_Error(msg)

        except KeyboardInterrupt:
            print("Detected Keyboard Interrupt. Quitting...")
            

        finally:
            consumer.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-host','--host_add', help='external ip address of the k8s cluster')
    args = parser.parse_args()
    topic = ["fashion-mnist-kafka-stream"]

    
    # connect to mongodb
    client = MongoClient('mongodb://localhost:27017')
    db = client['kafka-stream-records']
    
    
  
    consumer_thread = ConsumerThread( topic, db,args.host_add)
    
