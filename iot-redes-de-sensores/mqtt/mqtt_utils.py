BROKER_ADDRESS: str = "diegomont.com"
BROKER_PORT: int = 1883

TOPIC_1: str = "/diego/sensor1"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC_1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))