# order_service/app.py
from flask import Flask, request, jsonify
from confluent_kafka import Producer
import os

app = Flask(__name__)
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
producer = Producer({'bootstrap.servers': kafka_broker})

@app.route('/create-order', methods=['POST'])
def create_order():
    order_data = request.json
    order_id = order_data.get('id')
    producer.produce('orders', key=order_id, value=str(order_data))
    producer.flush()
    return jsonify({"status": "Order created", "order_id": order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)