from kafka import KafkaProducer, KafkaConsumer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

KAFKA_TOPIC=os.environ.get("KAFKA_TOPIC","orders")
# Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,  
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="inventory-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)