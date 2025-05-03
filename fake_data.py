from kafka import KafkaProducer
import json
import time

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize message as JSON
)

# Test data to simulate document titles
test_titles = [
    {"title": "Introduction to Artificial Intelligence", "lang": "fr"},
    {"title": "Understanding Deep Learning", "lang": "fr"},
    {"title": "Machine Learning in Practice", "lang": "fr"},
    {"title": "Big Data and Data Analytics", "lang": "fr"},
    {"title": "Cloud Computing and its Impact", "lang": "fr"}
]

# Send test data to the 'titles-to-translate' Kafka topic
for doc_title in test_titles:
    print(f"Sending: {doc_title}")
    producer.send('titles-to-translate', value=doc_title)
    time.sleep(1)  # Pause for 1 second between sends to avoid flooding the topic

# Make sure all messages are sent
producer.flush()

# Close the producer
producer.close()
print("✅ Sent test titles to Kafka.")
