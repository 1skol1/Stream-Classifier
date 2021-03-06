
# Stream-Classifier

An end-to-end implementation of a scalable real-time image streaming & classification service. Apache Kafka & Google Pub/Sub is used for streaming purposes & tf-serving model deployed in GKE is used for classification.

## Data-flow diagram
![alt text](https://github.com/1skol1/Stream-Classifier/blob/main/Stream-Classifier.jpg?raw=true)


## Folder Structure

```bash
.
├── kafka-stack-docker-compose                                # folder containing file to spin up kafka server
│   └── zk-single-kafka-single.yml
├── tensorflow-training                                       # folder containing files to train the model & exported model file
│   ├── exported_model
│   │   └── 1
│   │       ├── assets
│   │       ├── saved_model.pb
│   │       └── variables
│   │           ├── variables.data-00000-of-00001
│   │           └── variables.index
│   ├── model.py
│   └── trainer.py
├── tf-serving                                                # folder cointaining files to run & load test the model server
│   ├── locust
│   │   ├── request-body.json
│   │   ├── tasks.py
│   │   └── test-config.json
│   ├── serving
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── serving-k8s.sh
├── README.md
├── Stream-Classifier.jpg
├── ankle_boot.jpeg                                           # image used in request
├── client.py                                                 # python client to produce streamof requests
├── consumer_app_kafka.py                                     # consumer script for kafka
├── consumer_app_pubsub.py                                    # consumer script for pub/sub
├── producer_app.py                                           # fastAPI server for processing requests
├── tf_helper.py                                              # scritp for model prediction
├── unified.py                                                # unified api for producing & consuming kafka/pubsub messages
└── utils.py                                                  # utility functions

```
## Run Locally

Clone the project

```bash
  git clone https://github.com/1skol1/Stream-Classifier.git
```

Go to the project directory

```bash
  cd Stream-Classifier
```

Create a new conda environment

```bash
  conda env create -f environment.yml 
```

## Install Cloud SDK 

  Install Cloud SDK and login to your google account and create or choose a GCP project.
  Follow this guide: https://cloud.google.com/sdk/docs/quickstart
  
  And then create a environment variable of your project-id to be used when running the fastaAPI server & pubsub consumer.

```bash
  conda activate vectorai
  conda env config vars set GOOGLE_CLOUD_PROJECT="<your-project-id>"
  # re-activate the env after this & the check by running "echo $GOOGLE_CLOUD_PROJECT"
```

## Train the model

  There's already a trained model ready to be deployed under exported_model dir. You can directly upload this model or retrain it or train a new model. 
  To re-train the fashion-mnist model do this:
  * If there are changes you want to make in the model, pls update the model.py .
  * Then run the trainer.py, following are the arguments to be passed :
  ```bash
  usage: trainer.py [-h] -df DATA_FLAG -med MODEL_EXPORT_DIR [-train DATA_DIR_TRAIN] [-test DATA_DIR_TEST]
                  [-bs BATCH_SIZE] [-ih IMG_HEIGHT] [-iw IMG_WIDTH] [-ic IMG_CHANNEL]

optional arguments:
  -h, --help            show this help message and exit
  -df DATA_FLAG, --data_flag DATA_FLAG
                        0 for fashion_mnist, 1 for other multiclass dataset
  -med MODEL_EXPORT_DIR, --model_export_dir MODEL_EXPORT_DIR
                        path of parent directory where you want to store the exported model
  -train DATA_DIR_TRAIN, --data_dir_train DATA_DIR_TRAIN
                        path to training dataset directory
  -test DATA_DIR_TEST, --data_dir_test DATA_DIR_TEST
                        path to test/eval dataset directory
  -bs BATCH_SIZE, --batch_size BATCH_SIZE
                        batch size to be used while training
  -ih IMG_HEIGHT, --img_height IMG_HEIGHT
                        height of images in the dataset
  -iw IMG_WIDTH, --img_width IMG_WIDTH
                        width of images in the dataset
  -ic IMG_CHANNEL, --img_channel IMG_CHANNEL
                        no of color channels for the image,for RGB its 3, for grayscale its 1
  ```
  
  To train the a new model on new dataset do this :
  * Update the model.py.
  * Then run the trainer.py, with the arguments shown above.
  
  Export the trained model to a gcp bucket :
```bash
  export MODEL_BUCKET=${GOOGLE_CLOUD_PROJECT}-bucket
  gsutil mb gs://${MODEL_BUCKET}
  gsutil -r cp exported_model gs://${MODEL_BUCKET}
```

  **Make sure to grant IAM permissions to the compute engine service account to the gcp bucket.** 

## Pub/Sub Authentication

  * go to Google Developers Console and create a new project.
  * Enable the "Google Cloud Pub/Sub" API under "APIs & auth > APIs."
  * Go to "Credentials" and create a new Service Account.
  * Select "Generate new JSON key", then download a new JSON file.
  * Rename the downloaded JSON to "service-account-info.json" & place it in this repo's folder.

## Setting up Model Server

  To setup the model server:
  
  * Open the configmap.yaml file & change the "MODEL_PATH" to the path to your model bucket


## Install Docker & Docker-Compose

   Install Docker & Docker-Compose as we'll use it to run kafka & mongodb.
   https://docs.docker.com/engine/install/ubuntu/ 
   https://docs.docker.com/compose/install/
   
   To start mongodb container
```bash
  docker volume create data-mongodb       # to create a volume named data-mongodb
  docker run -v data-mongodb:/data/db -p 27017:27017 --name mongodb -d mongo        # this will automatically pull the MongoDB image and start the container.
```
  To stop mongodb container:
```bash
  docker stop mongodb     
```

  To start a kafka server run:
  
```bash
  cd kafka-stack-docker-compose
  docker-compose -f zk-single-kafka-single.yml up
```
  To stop :
```bash
  docker-compose -f zk-single-kafka-single.yml down
  docker-compose -f zk-single-kafka-single.yml rm   # to remove images
```

## Usage

  To start our whole system we'll first start our model server

```bash
  cd tf-serving
  chmod +x serving-k8s.sh
  ./serving-k8s.sh
  # when using first time it will ask you to enable compute & GKE api. You can re-run the script after a while.
  kubectl get svc image-classifier      # check the status of provisioning the service
  kubectl get pods                      # check the status of deployments
  # wait till a green checkmark - [x] appears on both the cluster & deployment in kubernetes dashboard in GCP. Might take 5-10 mins.
  # also note down the external ip of the cluster
```

  To load test the model server(Optional)
```bash
  cd locust
  locust -f tasks.py \
  --headless \
  --host http://${EXTERNAL_IP}:8501
```

  Start kafka server(do this in a new terminal) :
  
```bash
  cd kafka-stack-docker-compose
  docker-compose -f zk-single-kafka-single.yml up
```

  Start mongodb container :
  
```bash
  docker start mongodb     
```

  Start the fastAPI server(in a new terminal):
  
```bash
  uvicorn producer_app:app     
```

  Start the kafka consumer(in a new terminal):
```bash
   python consumer_app_kafka.py --host "<external ip of the cluster>"
```

  Start the pubsub consumer(in a new terminal):
 ```bash
   python consumer_app_pubsub.py --host "<external ip of the cluster>"
``` 
  
  Send the images ankle_boot.jpg as request using client.py :
 ```bash
   python client.py -api "<use /kafka-predict or /pubsub-predict>"
``` 
