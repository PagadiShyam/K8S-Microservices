from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
import os

app = Flask(__name__)
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
producer = Producer({'bootstrap.servers': kafka_broker})

@app.route('/create-order', methods=['POST'])
def create_order():
    order_data = request.json
    order_id = order_data.get('id')
    
    # Ensure valid JSON with double quotes
    try:
        json_payload = json.dumps(order_data, indent=2)
    except TypeError as e:
        return jsonify({"error": f"Invalid order data: {str(e)}"}), 400
    
    producer.produce('orders', key=str(order_id), value=json_payload)
    producer.flush()
    return jsonify({"status": "Order created", "order_id": order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)