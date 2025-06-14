import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from core.models import SensorData
from django.utils.timezone import now
import time

class Command(BaseCommand):
    help = 'MQTT Listener for latency data'

    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("Connected to test.mosquitto.org"))
                client.subscribe("latencyMonitor/#")
            else:
                self.stderr.write(f"Connection failed with code {rc}")

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                self.stdout.write(f"Received: {msg.topic} - {payload}")
                
                SensorData.objects.create(
                    topic=msg.topic,
                    payload=payload,
                    timestamp=now()
                )
            except Exception as e:
                self.stderr.write(f"Error processing message: {e}")

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        # Configurazione connessione al broker pubblico
        broker_url = "test.mosquitto.org"
        broker_port = 1883
        topic = "latencyMonitor/#"

        self.stdout.write(self.style.WARNING(f"Connecting to {broker_url} on topic {topic}..."))
        
        try:
            client.connect(broker_url, broker_port, 60)
            self.stdout.write(self.style.SUCCESS("MQTT listener started successfully"))
            client.loop_forever()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to start MQTT listener: {e}"))