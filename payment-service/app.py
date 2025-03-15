# payment_service/app.py
from flask import Flask
from confluent_kafka import Consumer, Producer
import os
import json

app = Flask(__name__)
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': 'payment-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['orders'])

producer = Producer({'bootstrap.servers': kafka_broker})

def process_payment(order):
    # Simulate payment processing
    order['payment_status'] = 'completed'
    return order

def kafka_poll():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        order = json.loads(msg.value().decode('utf-8'))
        processed_order = process_payment(order)
        producer.produce('payments', key=order['id'], value=json.dumps(processed_order))
        producer.flush()

if __name__ == '__main__':
    # Run consumer in background (use threading in production)
    import threading
    threading.Thread(target=kafka_poll, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)