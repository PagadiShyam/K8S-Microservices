from flask import Flask
from confluent_kafka import Consumer, Producer
import os
import json
import logging

app = Flask(__name__)
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': 'payment-group',
    'auto.offset.reset': 'earliest',
    'max.poll.interval.ms': 600000  # Increase if processing takes time
})

producer = Producer({'bootstrap.servers': kafka_broker})

def process_payment(order):
    try:
        # Simulate payment logic
        order['payment_status'] = 'completed' if order.get('amount', 0) <= 1000 else 'failed'
        return order
    except KeyError as e:
        logger.error(f"Missing key in order: {str(e)}")
        return None

def kafka_poll():
    consumer.subscribe(['orders'])
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            # Safely decode and parse
            raw_value = msg.value()
            if not raw_value:
                logger.warning("Received empty message")
                continue

            try:
                order = json.loads(raw_value.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {raw_value} | Error: {str(e)}")
                continue

            processed_order = process_payment(order)
            if processed_order:
                producer.produce('payments', key=str(order['id']), value=json.dumps(processed_order))
                producer.flush()

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == '__main__':
    import threading
    threading.Thread(target=kafka_poll, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)