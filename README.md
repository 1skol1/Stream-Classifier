
# Stream-Classifier

An end-to-end implementation of a scalable real-time image streaming & classification service. Apache Kafka & Google Pub/Sub is used for streaming purposes & tf-serving model deployed in GKE is used for classification.




## Folder Structure

```bash
.
├── ankle_boot.jpeg
├── client.py
├── config.py
├── consumer_app_kafka.py
├── consumer_app_pubsub.py
├── fashion-loader.py
├── frame-0.jpeg
├── kafka-stack-docker-compose
│   ├── full-stack.yml
│   ├── LICENSE
│   ├── README.md
│   ├── test.sh
│   ├── zk-multiple-kafka-multiple-schema-registry.yml
│   ├── zk-multiple-kafka-multiple.yml
│   ├── zk-multiple-kafka-single.yml
│   ├── zk-single-kafka-multiple.yml
│   └── zk-single-kafka-single.yml
├── producer_app.py
├── __pycache__
│   ├── config.cpython-39.pyc
│   ├── producer_app.cpython-39.pyc
│   ├── tf_helper.cpython-39.pyc
│   ├── unified.cpython-39.pyc
│   └── utils.cpython-39.pyc
├── service-account-info.json
├── tensorflow-training
│   ├── exported_model
│   │   └── 1
│   │       ├── assets
│   │       ├── saved_model.pb
│   │       └── variables
│   │           ├── variables.data-00000-of-00001
│   │           └── variables.index
│   ├── model.py
│   ├── __pycache__
│   │   └── model.cpython-39.pyc
│   └── trainer.py
├── tf_helper.py
├── tf-serving
│   ├── locust
│   │   ├── __pycache__
│   │   │   └── tasks.cpython-39.pyc
│   │   ├── request-body.json
│   │   ├── tasks.py
│   │   └── test-config.json
│   ├── serving
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── serving-k8s.sh
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

