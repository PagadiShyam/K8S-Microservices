# notification_service/app.py
from flask import Flask
from confluent_kafka import Consumer
import os
import json

app = Flask(__name__)
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': 'notification-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['payments'])

def send_notification(payment_data):
    # Simulate sending email/SMS
    print(f"Notification: Order {payment_data['id']} payment {payment_data['payment_status']}")

def kafka_poll():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        payment = json.loads(msg.value().decode('utf-8'))
        send_notification(payment)

if __name__ == '__main__':
    import threading
    threading.Thread(target=kafka_poll, daemon=True).start()
    app.run(host='0.0.0.0', port=5002)