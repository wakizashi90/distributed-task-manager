import pika
import time

# Retry connection to RabbitMQ
def get_rabbitmq_channel(retries=5, delay=5):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq')
            )
            channel = connection.channel()
            channel.queue_declare(queue='task_notifications')
            return channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Attempt {i + 1} of {retries} failed. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise pika.exceptions.AMQPConnectionError("Failed to connect to RabbitMQ after several attempts")


# Consume RabbitMQ messages and broadcast using the manager
def consume_messages(manager):
    channel = get_rabbitmq_channel()

    def callback(ch, method, properties, body):
        message = body.decode()
        print(f" [x] Received {message}")
        # Use the passed-in manager to broadcast the message
        manager.broadcast(message)

    channel.basic_consume(queue='task_notifications', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages.')
    channel.start_consuming()
