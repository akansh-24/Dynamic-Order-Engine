# kafka_service.py
from kafka import KafkaProducer, KafkaConsumer
import json
import time
import threading

ORDER_TOPIC = "order-events"
INVENTORY_TOPIC = "inventory-events"
KAFKA_BROKER = "kafka:9092"

# -------------------------------
# Producer Setup
# -------------------------------
def get_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Kafka Producer connected successfully")
            return producer
        except Exception as e:
            print("❌ Kafka Producer not ready, retrying in 5s...", e)
            time.sleep(5)

producer = get_producer()

def send_order_event(order_data: dict):
    """
    Send an order event to Kafka 'order-events' topic.
    """
    try:
        producer.send(ORDER_TOPIC, order_data)
        producer.flush()
        print(f"📤 Order event sent: {order_data}")
        return True
    except Exception as e:
        print("❌ Failed to send order event:", e)
        return False

# -------------------------------
# Consumer Setup
# -------------------------------
def get_consumer(topic: str, group_id: str):
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_BROKER,
                group_id=group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            print(f"✅ Connected to Kafka topic '{topic}' successfully")
            return consumer
        except Exception as e:
            print(f"❌ Kafka not ready for topic '{topic}', retrying in 5s...", e)
            time.sleep(5)

def consume_inventory_events(callback):
    """
    Start consuming messages from 'inventory-events'.
    The 'callback' function will be called with each event dict.
    """
    consumer = get_consumer(INVENTORY_TOPIC, "inventory-group")
    print("🟢 Listening to inventory-events...")
    for message in consumer:
        event = message.value
        print(f"📥 Received inventory event: {event}")
        try:
            callback(event)
        except Exception as e:
            print("❌ Error in inventory callback:", e)

# -------------------------------
# Helper to run consumer in a thread
# -------------------------------
def start_inventory_consumer_thread(callback):
    """
    Run inventory consumer in a separate daemon thread.
    """
    thread = threading.Thread(target=consume_inventory_events, args=(callback,))
    thread.daemon = True
    thread.start()
    print("🟢 Inventory consumer thread started")
    return thread

