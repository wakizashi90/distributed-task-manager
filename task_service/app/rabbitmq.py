import pika


def get_rabbitmq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()
    channel.queue_declare(queue='task_notifications')
    return channel

def publish_message(message: str):
    channel = get_rabbitmq_channel()
    channel.basic_publish(exchange='', routing_key='task_notifications', body=message)
    print(f" [x] Sent {message}")
