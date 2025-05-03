from kafka import KafkaConsumer, KafkaProducer
import json
from translator.gemini import translate_title  # Assuming you have a 'gemini.py' for translation
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
INPUT_TOPIC = os.getenv("INPUT_TOPIC", "titles-to-translate")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "translated-titles")

def run_translation_worker():
    consumer = KafkaConsumer(
        "titles-to-translate",  # Hardcode the topic name to avoid env issues
        bootstrap_servers="localhost:9092",  # Hardcode for now
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",       # Start from earliest messages
        enable_auto_commit=True,
        group_id="translation-service-test-1"  # Use a NEW group ID to re-read
    )

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda m: json.dumps(m).encode("utf-8")
    )

    print("📥 Listening on topic: titles-to-translate")
    for message in consumer:
        print("📦 Raw Kafka message:", message)
        data = message.value
        print("➡️ Decoded message value:", data)

        title = data.get("title")
        lang = data.get("lang", "fr")

        if not title:
            print("⚠️ Skipped message without title.")
            continue

        translated = translate_title(title, lang)
        print(f"✅ Translated: {translated}")

        producer.send("translated-titles", {"original": title, "translated": translated})
        producer.flush()
