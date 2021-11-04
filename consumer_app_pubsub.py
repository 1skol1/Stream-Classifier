import io
import os
import argparse
from concurrent.futures import TimeoutError

import numpy as np
import PIL.Image as Image
from pymongo import MongoClient

from tf_helper import get_model_prediction, get_stub
from unified import pubsub
from utils import *


def main(subscriber,subscription_path,host):

    def callback(message):
        
        
        print("\nCreate RPC connection ...")
        input_img = message.data
        image = Image.open(io.BytesIO(input_img))
        image = np.array(image)
        image = np.reshape(image, image.shape + (1,))
        stub = get_stub(host)
        model_prediction = get_model_prediction(image, stub)
        

        
        if message.attributes:
            
            frame_id = message.attributes.get("video_id")
            timestamp = message.attributes.get("timestamp")
        doc = {
                                "frame_id": frame_id,
                                "label": model_prediction,
                                "timestamp": timestamp
                           }
        collection.insert_one(doc)

        message.ack()         


    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}')


    with subscriber:                                                
        try:
            try:
                streaming_pull_future.result()    
            except KeyboardInterrupt:
                print("Detected Keyboard Interrupt. Quitting...")   
                streaming_pull_future.cancel()                   
        except TimeoutError:
            streaming_pull_future.cancel()                          # trigger the shutdown
            streaming_pull_future.result()     




    
    
if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host','--host_add', help='external ip address of the k8s cluster')
    args = parser.parse_args()
    credentials_path = 'service-account-info.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    subscriber,subscription_path = pubsub.create_subscription(os.getenv('GOOGLE_CLOUD_PROJECT'),'fashion-mnist-pubsub-stream')
    client = MongoClient('mongodb://localhost:27017')
    db = client['pubsub-stream-records']
    collection = db['test_collection']
    main(subscriber,subscription_path,args.host_add)
    

