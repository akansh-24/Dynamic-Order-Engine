#!/usr/bin/env python3
import socket, time, os, sys

bootstrap = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
try:
    host, port = bootstrap.split(":")
    port = int(port)
except Exception:
    print("Invalid KAFKA_BOOTSTRAP_SERVERS:", bootstrap)
    sys.exit(1)

retries = int(os.environ.get("WAIT_RETRIES", "20"))
delay = float(os.environ.get("WAIT_DELAY", "1"))

for attempt in range(1, retries + 1):
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"[ok] Connected to Kafka at {host}:{port}")
            sys.exit(0)
    except Exception as e:
        print(f"[waiting {attempt}/{retries}] {host}:{port} not ready: {e}")
        time.sleep(delay)

print(f"[failed] Could not connect to Kafka at {host}:{port} after {retries} attempts")
sys.exit(1)
