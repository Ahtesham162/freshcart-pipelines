
import os
import sys
import json
import pika
from dotenv import load_dotenv

load_dotenv()

AMQP_URL = os.getenv("AMQP_URL")

if not AMQP_URL:
    raise ValueError("AMQP_URL not found in .env")

if len(sys.argv) != 3:
    print("Usage: python stream/driver.py NAME PATTERN")
    sys.exit(1)

name = sys.argv[1]
pattern = sys.argv[2]

connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=pattern
)

print(f"{name} listening for: {pattern}")

def callback(ch, method, properties, body):
    try:
        event = json.loads(body)

        if not event.get("zone"):
            print(f"{name}: REJECTED - missing zone | {event}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        print(f"{name}: Received {method.routing_key} | {event}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (json.JSONDecodeError, TypeError):
        print(f"{name}: REJECTED - invalid JSON")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\n{name} stopped.")
finally:
    connection.close()
