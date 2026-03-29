"""Event publisher — sends messages to RabbitMQ (asynchronous, cross-quantum)."""

import json
import pika

RABBITMQ_HOST = "rabbitmq"


def publish_event(queue: str, payload: dict) -> None:
    """Publish an event to a named queue.

    This is the ASYNC boundary that separates the Bidding quantum
    from the Payment and Notification quanta.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    connection.close()
