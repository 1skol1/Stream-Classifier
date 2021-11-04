'''
    Unified API of both Apache Kafka & Google Pub/Sub for easy to use implementation in 
    producer & consumer apps.
'''

from confluent_kafka import Consumer, KafkaError, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from google import api_core
from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud import pubsub_v1

from utils import *


class kafka:


    producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'enable.idempotence': True,
    'acks': 'all',
    'retries': 100,
    'max.in.flight.requests.per.connection': 5,
    'compression.type': 'snappy',
    'linger.ms': 5,
    'batch.num.messages': 32
    }

    consumer_config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'kafka-fashion-mnist-stream',
    'enable.auto.commit': False,
    'default.topic.config': {'auto.offset.reset': 'earliest'}
    }


    def __init__(self,ac_config) -> None:
        self.ac_conif = ac_config
        self.admin_client = AdminClient(self.ac_conif)


    def create_topic(self,topic_name:list[str],no_replicas:int,no_partitions:int) -> None:
        """Create a new kafka topic."""

        topic_list = [NewTopic(topic, no_partitions, no_replicas) for topic in topic_name]
        fs = self.admin_client.create_topics(topic_list)

        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))


    def delete_topics(self, topics)-> None:
        """ delete topics """

        # Call delete_topics to asynchronously delete topics, a future is returned.
        # By default this operation on the broker returns immediately while
        # topics are deleted in the background. But here we give it some time (30s)
        # to propagate in the cluster before returning.
        #
        # Returns a dict of <topic,future>.
        fs = self.admin_client.delete_topics(topics, operation_timeout=30)

        # Wait for operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} deleted".format(topic))
            except Exception as e:
                print("Failed to delete topic {}: {}".format(topic, e))


    def kafka_produce(self)-> object:
        """Publishes messages ."""

        self.producer = Producer(self.producer_config)
        return self.producer

        
    @staticmethod
    def kafka_consumer(topic)-> object:
        """Create a new consumer on the given topic."""

        consumer = Consumer(kafka.consumer_config)
        consumer.subscribe(topic)
        return consumer 


    def EOF_Error(self,msg)-> None:
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                        .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))




class pubsub:


    custom_retry = api_core.retry.Retry(
        initial=0.250,  # seconds (default: 0.1)
        maximum=90.0,  # seconds (default: 60.0)
        multiplier=1.45,  # default: 1.3
        deadline=300.0,  # seconds (default: 60.0)
        predicate=api_core.retry.if_exception_type(
            api_core.exceptions.Aborted,
            api_core.exceptions.DeadlineExceeded,
            api_core.exceptions.InternalServerError,
            api_core.exceptions.ResourceExhausted,
            api_core.exceptions.ServiceUnavailable,
            api_core.exceptions.Unknown,
            api_core.exceptions.Cancelled,
        ),
    )


    def __init__(self,project_id:str, topic_id:str):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        self.topic_name = None


    def create_topic(self) -> None:
        """Create a new Pub/Sub topic."""

        try:
            self.topic = self.publisher.create_topic(request={"name": self.topic_path})
            print(f"Created topic: {self.topic.name}")
        except AlreadyExists:
            print(f"{self.topic_id} already exists.")
            
            


    def delete_topic(self) -> None:
        """Deletes an existing Pub/Sub topic."""
        try:
            self.publisher.delete_topic(self.topic_path)
            print(f"Topic deleted: {self.topic_path}")
        except NotFound:
            pass
        
        
    def pubsub_produce(self) -> str:
        """Publishes messages with custom retry settings."""

        return self.publisher,self.topic_path

    @staticmethod
    def create_subscription(project_id,subscription_id: str) -> object:
        """Create a new pull subscription on the given topic."""

        
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        try:
            subscriber.create_subscription(
            name=subscription_path, topic='projects/vector-ai-330615/topics/fashion-mnist-pubsub-stream')
        except AlreadyExists:
            print(f"{subscription_path} already exists.")
        finally:
            return subscriber, subscription_path

        


    def list_topics(self) -> None:
        """Lists all Pub/Sub topics in the given project."""

        publisher = pubsub_v1.PublisherClient()
        project_path = f"projects/{self.project_id}"

        for topic in publisher.list_topics(request={"project": project_path}):
            print(topic)


    def get_custom_retry(self):
        return self.custom_retry
