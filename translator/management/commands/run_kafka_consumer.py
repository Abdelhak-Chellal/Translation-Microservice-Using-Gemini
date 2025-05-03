# translator/management/commands/run_kafka_consumer.py
from django.core.management.base import BaseCommand
from translator.kafka_worker import run_translation_worker

class Command(BaseCommand):
    help = "Starts the Kafka consumer and listens for incoming titles to translate."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Kafka Consumer...\n")
        try:
            run_translation_worker()
        except KeyboardInterrupt:
            self.stdout.write("Kafka Consumer stopped.\n")
