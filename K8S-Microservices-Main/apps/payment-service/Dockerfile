FROM python:3.9-slim

 
# Install netcat and copy the script
RUN apt-get update && apt-get install -y netcat-openbsd
COPY wait-for-kafka.sh .
RUN chmod +x wait-for-kafka.sh
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script and app code
COPY wait-for-kafka.sh .
COPY . .

# Run script first, then start the app
CMD ["./wait-for-kafka.sh", "python", "app.py"]