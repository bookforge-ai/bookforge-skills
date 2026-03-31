"""Notification Service worker — consumes events from RabbitMQ.

Architecture characteristics: AVAILABILITY (notifications should always be deliverable).
Communication: asynchronous consumer only — no synchronous coupling.
This is its own quantum with independent deployment.
"""

import json
import time
import pika
from sender import send_notification

RABBITMQ_HOST = "rabbitmq"
QUEUE = "notification_queue"


def on_message(channel, method, properties, body):
    """Handle incoming notification event."""
    event = json.loads(body)
    print(f"[Notification] Received: {event}")
    send_notification(event)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
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
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)
    print("[Notification] Waiting for events...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
