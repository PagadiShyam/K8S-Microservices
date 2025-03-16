#!/bin/sh

# Fail script on any error
set -e

# Host and port of Kafka broker
KAFKA_HOST="kafka"
KAFKA_PORT="9092"

echo "Waiting for Kafka at $KAFKA_HOST:$KAFKA_PORT..."

# Loop until Kafka is reachable
while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
  sleep 1
done

echo "Kafka is ready! Starting service..."
exec "$@"