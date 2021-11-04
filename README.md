
# Stream-Classifier

An end-to-end implementation of a scalable real-time image streaming & classification service. Apache Kafka & Google Pub/Sub is used for streaming purposes & tf-serving model deployed in GKE is used for classification.

# Data-flow diagram
![alt text](https://github.com/1skol1/Stream-Classifier/blob/main/Stream-Classifier.jpg?raw=true)


## Folder Structure

```bash
.
├── kafka-stack-docker-compose
│   └── zk-single-kafka-single.yml
├── tensorflow-training
│   ├── exported_model
│   │   └── 1
│   │       ├── assets
│   │       ├── saved_model.pb
│   │       └── variables
│   │           ├── variables.data-00000-of-00001
│   │           └── variables.index
│   ├── model.py
│   └── trainer.py
├── tf-serving
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
├── ankle_boot.jpeg
├── client.py
├── consumer_app_kafka.py
├── consumer_app_pubsub.py
├── producer_app.py
├── tf_helper.py
├── unified.py
└── utils.py

```
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```


## Usage/Examples

```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```


## Deployment

To deploy this project run

```bash
  npm run deploy
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

