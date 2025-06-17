import time, random, paho.mqtt.client as mqtt

BROKER = 'test.mosquitto.org'  
PORT = 1883
TOPIC = 'latencyMonitor/iPhone13'

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def generate_data():
    num1 = random.randint(100, 1000)
    num2 = random.randint(100, 1000)
    return f"{num1},{num2}"

def main():
    try:
        while True:
            message = generate_data()
            client.publish(TOPIC, message)
            print(f"Published: {message}")
            time.sleep(1) 
    except KeyboardInterrupt:
        print("Programma interrotto")

if __name__ == "__main__":
    main()
