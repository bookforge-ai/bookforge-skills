"""Payment Service worker — consumes auction_closed events from RabbitMQ.

Architecture characteristics: RELIABILITY (payments must not be lost), SECURITY.
Communication: asynchronous consumer only — no synchronous coupling to other services.
This is its own quantum with independent deployment.
"""

import json
import time
import pika
from processor import process_payment

RABBITMQ_HOST = "rabbitmq"
QUEUE = "payment_queue"


def on_message(channel, method, properties, body):
    """Handle incoming payment event with acknowledgment (reliability)."""
    event = json.loads(body)
    print(f"[Payment] Received: {event}")
    try:
        process_payment(event)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f"[Payment] FAILED: {exc} — will retry")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    # Retry connection — RabbitMQ may start after this service
    for attempt in range(10):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(2)
    else:
        raise RuntimeError("Cannot connect to RabbitMQ")

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)  # reliability: one at a time
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)
    print("[Payment] Waiting for events...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
