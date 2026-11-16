
import os
import json
import time
import uuid
import random
from datetime import datetime, timezone

import pika
from dotenv import load_dotenv

load_dotenv()

AMQP_URL = os.getenv("AMQP_URL")
if not AMQP_URL:
    raise ValueError("AMQP_URL not found in .env")

connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

cities = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "velachery", "adyar"]
}

types = ["ride", "food"]

count = 0

try:
    while True:
        city = random.choice(list(cities.keys()))
        zone = random.choice(cities[city])
        event_type = random.choice(types)

        event = {
            "id": str(uuid.uuid4()),
            "city": city,
            "type": event_type,
            "ts": datetime.now(timezone.utc).isoformat()
        }

        if (count + 1) % 10 != 0:
            event["zone"] = zone

        routing_key = f"{city}.{zone}.{event_type}"

        channel.basic_publish(
            exchange="rapido-dispatch",
            routing_key=routing_key,
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
        )

        count += 1
        print(f"Published #{count}: {routing_key} | {event}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nDispatcher stopped.")

finally:
    connection.close()
